"""
Module for cleaning and processing raw datasets, and loading them into an SQLite database.
"""
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import os
import glob
import sqlite3
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

def clean_data():
    """
    Clean the CSV datasets by handling missing values, dates, and anomalies.
    Saves the cleaned datasets to the 'data/processed' directory.
    """
    os.makedirs('data/processed', exist_ok=True)
    
    nav_df = pd.read_csv('data/02_nav_history.csv')
    nav_df['date'] = pd.to_datetime(nav_df['date'])
    nav_df = nav_df.sort_values(by=['amfi_code', 'date'])
    
    def fill_missing_dates(group):
        min_date = group['date'].min()
        max_date = group['date'].max()
        full_date_range = pd.date_range(start=min_date, end=max_date)
        group = group.set_index('date').reindex(full_date_range)
        group['amfi_code'] = group['amfi_code'].ffill()
        group['nav'] = group['nav'].ffill()
        group = group.reset_index().rename(columns={'index': 'date'})
        return group
    
    nav_df = nav_df.groupby('amfi_code', group_keys=False).apply(fill_missing_dates)
    nav_df = nav_df.drop_duplicates(subset=['amfi_code', 'date'])
    nav_df = nav_df[nav_df['nav'] > 0]
    nav_df['date'] = nav_df['date'].dt.strftime('%Y-%m-%d')
    nav_df.to_csv('data/processed/02_nav_history.csv', index=False)
    
    tx_df = pd.read_csv('data/08_investor_transactions.csv')
    tx_df['transaction_type'] = tx_df['transaction_type'].str.capitalize()
    tx_df = tx_df[tx_df['amount_inr'] > 0]
    tx_df['transaction_date'] = pd.to_datetime(tx_df['transaction_date']).dt.strftime('%Y-%m-%d')
    tx_df = tx_df[tx_df['kyc_status'].isin(['Verified', 'Pending'])]
    tx_df.to_csv('data/processed/08_investor_transactions.csv', index=False)
    
    perf_df = pd.read_csv('data/07_scheme_performance.csv')
    num_cols = ['return_1yr_pct', 'return_3yr_pct', 'return_5yr_pct', 'benchmark_3yr_pct', 'alpha', 'beta', 'sharpe_ratio', 'sortino_ratio', 'std_dev_ann_pct', 'max_drawdown_pct', 'aum_crore']
    for col in num_cols:
        perf_df[col] = pd.to_numeric(perf_df[col], errors='coerce')
    perf_df['is_anomaly'] = perf_df[num_cols].isnull().any(axis=1)
    perf_df = perf_df[(perf_df['expense_ratio_pct'] >= 0.1) & (perf_df['expense_ratio_pct'] <= 2.5)]
    perf_df.to_csv('data/processed/07_scheme_performance.csv', index=False)

    for file in glob.glob('data/*.csv'):
        basename = os.path.basename(file)
        if basename not in ['02_nav_history.csv', '08_investor_transactions.csv', '07_scheme_performance.csv']:
            df = pd.read_csv(file)
            if 'date' in df.columns:
                try:
                    df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
                except:
                    pass
            if 'launch_date' in df.columns:
                try:
                    df['launch_date'] = pd.to_datetime(df['launch_date']).dt.strftime('%Y-%m-%d')
                except:
                    pass
            df.to_csv(f'data/processed/{basename}', index=False)

def generate_dim_date():
    """
    Generate a dimension table for dates based on NAV and transaction datasets.
    """
    nav_df = pd.read_csv('data/processed/02_nav_history.csv')
    tx_df = pd.read_csv('data/processed/08_investor_transactions.csv')
    
    dates = pd.concat([nav_df['date'], tx_df['transaction_date']]).dropna().unique()
    dates = pd.to_datetime(dates)
    
    dim_date = pd.DataFrame({'date': dates})
    dim_date['date_str'] = dim_date['date'].dt.strftime('%Y-%m-%d')
    dim_date['day'] = dim_date['date'].dt.day
    dim_date['month'] = dim_date['date'].dt.month
    dim_date['year'] = dim_date['date'].dt.year
    dim_date['quarter'] = dim_date['date'].dt.quarter
    dim_date['day_of_week'] = dim_date['date'].dt.dayofweek
    dim_date['is_weekend'] = dim_date['day_of_week'].isin([5, 6])
    
    dim_date['date'] = dim_date['date_str']
    dim_date = dim_date.drop(columns=['date_str'])
    dim_date.to_csv('dim_date_temp.csv', index=False)

def load_to_sqlite():
    """
    Load all processed datasets into an SQLite database.
    """
    db_path = 'bluestock_mf.db'
    if os.path.exists(db_path):
        os.remove(db_path)
        
    conn = sqlite3.connect(db_path)
    with open('schema.sql', 'r') as f:
        conn.executescript(f.read())
    conn.close()

    engine = create_engine(f'sqlite:///{db_path}')
    
    file_table_mapping = {
        '01_fund_master.csv': 'dim_fund',
        '02_nav_history.csv': 'fact_nav',
        '08_investor_transactions.csv': 'fact_transactions',
        '07_scheme_performance.csv': 'fact_performance',
        '03_aum_by_fund_house.csv': 'fact_aum',
        'dim_date_temp.csv': 'dim_date'
    }
    
    for basename, table_name in file_table_mapping.items():
        file_path = f'data/processed/{basename}' if 'dim_date_temp' not in basename else basename
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            df.to_sql(table_name, con=engine, if_exists='append', index=False)
            
    if os.path.exists('dim_date_temp.csv'):
        os.remove('dim_date_temp.csv')

if __name__ == "__main__":
    clean_data()
    generate_dim_date()
    load_to_sqlite()
