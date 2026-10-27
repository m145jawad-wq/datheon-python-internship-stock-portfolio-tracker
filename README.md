Stock Portfolio Performance Tracker 📈A lightweight Python command-line utility that tracks real-time stock portfolio performance, calculates capital valuations and percentage gains/losses, and logs transaction summaries to a standard CSV file.   🌟 Key FeaturesPortfolio Input & Tracking: Enter stock tickers, total quantity of shares, and purchase buy prices.Price Lookup: Automatically loads current stock market prices from a dataset (sp500_tickers.csv) or falls back to standard mock prices.Valuation Calculations:Total invested capital vs current market value.Individual gain/loss amount ($) and percentage (%) per holding.Portfolio-wide net gain/loss ($ and %).CSV Performance Logging: Exports and logs the performance summary into portfolio_summary.csv using Python's built-in csv module.   Formatted Console Output: Displays a neat, aligned terminal dashboard table.📂 Project StructurePlaintext.
├── portfolio.py          # Main Python script for valuation and logging
├── sp500_tickers.csv     # Input dataset containing current market prices
├── portfolio_summary.csv # Auto-generated CSV performance report
└── README.md             # Project documentation
⚙️ How to RunRequirementsPython 3.x installed (no external libraries needed, uses standard modules csv and os).StepsMake sure portfolio.py and sp500_tickers.csv are in the same folder.Open your terminal or command prompt and run:Bashpython portfolio.py
Enter your holdings when prompted (Ticker, Shares, Buy Price).Type done or press Enter to complete your input and process the portfolio summary.📊 Sample Output FormatTerminal Output:Plaintext================================================================================
                      PORTFOLIO PERFORMANCE SUMMARY                      
================================================================================
Ticker   Shares     Buy Price    Cur Price    Value          Gain/Loss     
--------------------------------------------------------------------------------
AAPL     10.00      $150.00      $185.50      $1855.00       +$355.00 (+23.67%)
MSFT     5.00       $380.00      $420.25      $2101.25       +$201.25 (+10.59%)
TSLA     8.00       $200.00      $240.50      $1924.00       +$324.00 (+20.25%)
--------------------------------------------------------------------------------
Total Invested Capital : $5,000.00
Total Portfolio Value  : $5,880.25
Overall Profit/Loss    : +$880.25 (+17.61%)
================================================================================

[SUCCESS] Performance summary logged to 'portfolio_summary.csv' successfully!
Generated CSV (portfolio_summary.csv):Code snippetTicker,Shares,Buy Price ($),Current Price ($),Invested Capital ($),Current Value ($),Gain/Loss ($),Gain/Loss (%)
AAPL,10.00,150.00,185.50,1500.00,1855.00,355.00,23.67%
MSFT,5.00,380.00,420.25,1900.00,2101.25,201.25,10.59%
TSLA,8.00,200.00,240.50,1600.00,1924.00,324.00,20.25%
