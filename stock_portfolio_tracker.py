import csv
import os
import sys

# Built-in fallback market data when external file is missing
DEFAULT_MARKET_PRICES = {
    "AAPL": 185.50,
    "MSFT": 420.25,
    "GOOGL": 175.00,
    "AMZN": 180.75,
    "TSLA": 240.50,
    "NVDA": 125.30,
    "META": 490.10,
    "NFLX": 620.00,
    "AMD": 160.40,
    "INTC": 31.20
}

DATASET_FILE = "sp500_tickers.csv"
SUMMARY_FILE = "portfolio_summary.csv"


def load_market_prices(filepath: str = DATASET_FILE) -> dict:
    """
    Loads ticker prices from 'sp500_tickers.csv' using Python's standard csv module.
    Falls back gracefully to default prices if file is missing or unreadable.
    """
    market_prices = DEFAULT_MARKET_PRICES.copy()
    
    if os.path.exists(filepath):
        try:
            with open(filepath, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                count = 0
                for row in reader:
                    ticker = row.get("Ticker", "").strip().upper()
                    price_str = row.get("Price") or row.get("CurrentPrice") or row.get("MarketPrice")
                    if ticker and price_str:
                        try:
                            market_prices[ticker] = float(price_str)
                            count += 1
                        except ValueError:
                            continue
                print(f"[Info] Successfully loaded {count} ticker prices from '{filepath}'.")
        except Exception as e:
            print(f"[Warning] Failed to read '{filepath}' ({e}). Utilizing fallback dataset.")
    else:
        print(f"[Info] '{filepath}' not found. Utilizing default fallback prices.")

    return market_prices


def get_portfolio_inputs() -> dict:
    """
    Interactive prompt asking user for stock ticker, buy price, and share count.
    Saves and returns portfolio holdings in a structured dictionary.
    """
    portfolio = {}
    print("\n" + "=" * 60)
    print("        STOCK PORTFOLIO TRACKER - INPUT HOLDINGS")
    print("=" * 60)
    print("Enter your positions below. Type 'done' or press Enter to finish.\n")

    while True:
        try:
            ticker = input("Enter Stock Ticker Symbol (e.g. AAPL, MSFT): ").strip().upper()
            if not ticker or ticker == 'DONE':
                break

            shares_input = input(f"Enter number of shares for {ticker}: ").strip()
            if not shares_input:
                break
            shares = float(shares_input)

            buy_price_input = input(f"Enter buy price per share for {ticker} ($): ").strip()
            if not buy_price_input:
                break
            buy_price = float(buy_price_input)

            if shares <= 0 or buy_price <= 0:
                print("[Error] Share count and buy price must be positive numbers!\n")
                continue

            portfolio[ticker] = {
                "shares": shares,
                "buy_price": buy_price
            }
            print(f"[Added] {ticker}: {shares:,.2f} shares @ ${buy_price:,.2f} each.\n")

        except ValueError:
            print("[Error] Invalid entry. Please enter valid numeric values for shares and price.\n")

    return portfolio


def calculate_portfolio_performance(portfolio: dict, market_prices: dict):
    """
    Computes current valuation, dollar gain/loss, and percentage gain/loss per position
    as well as total invested capital vs current market value.
    """
    summary = []
    total_invested = 0.0
    total_current_val = 0.0

    for ticker, data in portfolio.items():
        shares = data["shares"]
        buy_price = data["buy_price"]
        
        # Look up current market price (fallback to buy price if missing)
        current_price = market_prices.get(ticker, buy_price)

        invested_val = shares * buy_price
        current_val = shares * current_price
        gain_loss = current_val - invested_val
        gain_loss_pct = (gain_loss / invested_val) * 100 if invested_val > 0 else 0.0

        total_invested += invested_val
        total_current_val += current_val

        summary.append({
            "ticker": ticker,
            "shares": shares,
            "buy_price": buy_price,
            "current_price": current_price,
            "invested_val": invested_val,
            "current_val": current_val,
            "gain_loss": gain_loss,
            "gain_loss_pct": gain_loss_pct
        })

    overall_gain_loss = total_current_val - total_invested
    overall_gain_loss_pct = (overall_gain_loss / total_invested) * 100 if total_invested > 0 else 0.0

    return summary, total_invested, total_current_val, overall_gain_loss, overall_gain_loss_pct


def export_and_append_to_csv(summary: list, filepath: str = SUMMARY_FILE):
    """
    Exports performance logs and appends results to 'portfolio_summary.csv' using standard csv module.
    Automatically creates headers if file does not exist.
    """
    headers = [
        "Ticker", "Shares", "Buy Price ($)", "Current Price ($)",
        "Invested Capital ($)", "Current Value ($)", "Gain/Loss ($)", "Gain/Loss (%)"
    ]
    
    file_exists = os.path.exists(filepath)

    try:
        with open(filepath, mode='a', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            
            # Write header row if file is brand new
            if not file_exists or os.path.getsize(filepath) == 0:
                writer.writerow(headers)

            for item in summary:
                writer.writerow([
                    item["ticker"],
                    f"{item['shares']:.2f}",
                    f"{item['buy_price']:.2f}",
                    f"{item['current_price']:.2f}",
                    f"{item['invested_val']:.2f}",
                    f"{item['current_val']:.2f}",
                    f"{item['gain_loss']:.2f}",
                    f"{item['gain_loss_pct']:.2f}%"
                ])
                
        print(f"\n[SUCCESS] Transaction summary logged & appended to '{filepath}'.")
    except Exception as e:
        print(f"[ERROR] Failed to export CSV file: {e}")


def display_console_output(summary: list, total_invested: float, total_current_val: float, 
                           overall_gain_loss: float, overall_gain_loss_pct: float):
    """
    Renders formatted visual summary in the console.
    """
    print("\n" + "=" * 82)
    print("                       PORTFOLIO PERFORMANCE SUMMARY                       ")
    print("=" * 82)
    print(f"{'Ticker':<8} {'Shares':<10} {'Buy Price':<12} {'Cur Price':<12} {'Market Value':<15} {'Gain/Loss':<16}")
    print("-" * 82)

    for item in summary:
        gl_str = f"${item['gain_loss']:>+9.2f} ({item['gain_loss_pct']:>+6.2f}%)"
        print(f"{item['ticker']:<8} {item['shares']:<10.2f} ${item['buy_price']:<11.2f} ${item['current_price']:<11.2f} ${item['current_val']:<14.2f} {gl_str}")

    print("-" * 82)
    print(f"Total Invested Capital : ${total_invested:,.2f}")
    print(f"Total Portfolio Value  : ${total_current_val:,.2f}")
    print(f"Overall Profit / Loss  : ${overall_gain_loss:+,.2f} ({overall_gain_loss_pct:+.2f}%)")
    print("=" * 82 + "\n")


def main():
    market_prices = load_market_prices()

    # Get holdings from user input
    portfolio = get_portfolio_inputs()

    # Default demo portfolio if user skips input
    if not portfolio:
        print("[Notice] No manual positions entered. Loading default sample holdings (AAPL, MSFT, TSLA, NVDA)...")
        portfolio = {
            "AAPL": {"shares": 10, "buy_price": 150.00},
            "MSFT": {"shares": 5, "buy_price": 380.00},
            "TSLA": {"shares": 8, "buy_price": 200.00},
            "NVDA": {"shares": 15, "buy_price": 110.00}
        }

    # Perform calculations
    summary, total_inv, total_val, gl, gl_pct = calculate_portfolio_performance(portfolio, market_prices)

    # Display results
    display_console_output(summary, total_inv, total_val, gl, gl_pct)

    # Export to CSV
    export_and_append_to_csv(summary)


if __name__ == "__main__":
    main()