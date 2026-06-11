# Bluestock Mutual Fund Analytics Capstone

## Project Overview
This project is an end-to-end data engineering and analytics pipeline for Indian Mutual Funds. It involves ingesting data from various sources (including live APIs), transforming and cleaning the data using Pandas, and loading it into a structured SQLite database. The project also features a Power BI dashboard for visualizing performance, AUM distribution, and investor trends.

## Setup Instructions
1. Ensure you have Python 3.8+ installed.
2. Clone this repository (or download the files).
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Optional: If you want to fetch live data or re-run the pipeline, ensure you have an active internet connection to reach `api.mfapi.in`.

## How to Run the ETL Pipeline
We have provided a master execution script that runs the entire pipeline end-to-end.
```bash
python run_pipeline.py
```
This script will sequentially:
1. Fetch live NAV data for selected mutual funds.
2. Load and explore the raw CSV datasets from the `data/` directory.
3. Clean and process the data, generating a centralized SQLite database (`bluestock_mf.db`) with a star schema design.

You can also run the recommender script to get fund recommendations based on risk appetite:
```bash
python recommender.py High
```

## How to Open the Dashboard
1. Ensure you have **Power BI Desktop** installed on your Windows machine.
2. Double-click the `bluestock_mf_dashboard.pbix` file located in the root directory.
3. The dashboard connects directly to the `bluestock_mf.db` SQLite database (you may need an SQLite ODBC driver if you plan to refresh data within Power BI).

## Dataset Descriptions
- **01_fund_master.csv**: Core details of mutual funds (AMFI code, scheme name, fund house, category, risk grade).
- **02_nav_history.csv**: Historical Net Asset Value records for various funds.
- **03_aum_by_fund_house.csv**: Assets Under Management distributed by fund house.
- **07_scheme_performance.csv**: Performance metrics (1yr, 3yr, 5yr returns, Sharpe ratio, etc.) for funds.
- **08_investor_transactions.csv**: Sample transactional data showing investor deposits and withdrawals.
- **bluestock_mf.db**: The final unified SQLite database containing cleaned fact and dimension tables.
