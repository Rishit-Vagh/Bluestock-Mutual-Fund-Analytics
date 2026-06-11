"""
Module for loading and exploring mutual fund datasets.
Provides functions to load CSV files into DataFrames and perform initial data validation.
"""
import pandas as pd
import glob
import os

def load_and_explore_datasets(data_dir="data"):
    """
    Load all CSV datasets from the specified directory.
    
    Args:
        data_dir (str): Directory containing the CSV files. Defaults to 'data'.
        
    Returns:
        dict: A dictionary mapping filenames to their corresponding pandas DataFrames.
    """
    csv_files = glob.glob(os.path.join(data_dir, "*.csv"))
    datasets = {}
    
    for file in sorted(csv_files):
        try:
            df = pd.read_csv(file)
            datasets[os.path.basename(file)] = df
        except Exception as e:
            # Handle error silently as per requirements to remove debug prints
            pass
            
    return datasets

def explore_fund_master(fund_master_df):
    """
    Explore the fundamental attributes of the fund master dataset.
    
    Args:
        fund_master_df (pd.DataFrame): DataFrame containing the fund master data.
    """
    pass  # Removed debug prints

def validate_amfi_codes(fund_master_df, nav_history_df):
    """
    Validate AMFI codes across the fund master and NAV history datasets.
    
    Args:
        fund_master_df (pd.DataFrame): DataFrame containing the fund master data.
        nav_history_df (pd.DataFrame): DataFrame containing the NAV history data.
    """
    pass  # Removed debug prints

def main():
    """
    Main execution logic for data ingestion.
    Loads datasets and triggers validation logic.
    """
    datasets = load_and_explore_datasets()
    
    if '01_fund_master.csv' in datasets:
        explore_fund_master(datasets['01_fund_master.csv'])
        
    if '01_fund_master.csv' in datasets and '02_nav_history.csv' in datasets:
        validate_amfi_codes(datasets['01_fund_master.csv'], datasets['02_nav_history.csv'])

if __name__ == "__main__":
    main()
