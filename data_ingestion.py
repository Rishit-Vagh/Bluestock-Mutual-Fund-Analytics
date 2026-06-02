import pandas as pd
import glob
import os

def load_and_explore_datasets(data_dir="data"):
    csv_files = glob.glob(os.path.join(data_dir, "*.csv"))
    print(f"Found {len(csv_files)} CSV datasets in {data_dir}.")
    
    datasets = {}
    
    for file in sorted(csv_files):
        print(f"\n--- Processing {os.path.basename(file)} ---")
        try:
            df = pd.read_csv(file)
            datasets[os.path.basename(file)] = df
            
            print("Shape:", df.shape)
            print("Data Types:\n", df.dtypes)
            print("Head:\n", df.head())
            
            # Check for anomalies
            anomalies = []
            if df.isnull().values.any():
                null_counts = df.isnull().sum()
                cols_with_nulls = null_counts[null_counts > 0].index.tolist()
                anomalies.append(f"Contains missing values in columns: {', '.join(cols_with_nulls)}.")
            if df.duplicated().any():
                anomalies.append(f"Contains {df.duplicated().sum()} duplicate rows.")
                
            if len(anomalies) == 0:
                print("Anomalies: None detected.")
            else:
                print("Anomalies:")
                for anomaly in anomalies:
                    print(f" - {anomaly}")
                    
        except Exception as e:
            print(f"Error loading {file}: {e}")
            
    return datasets

def explore_fund_master(fund_master_df):
    print("\n--- Exploring Fund Master ---")
    if 'fund_house' in fund_master_df.columns:
        print("Unique Fund Houses:\n", fund_master_df['fund_house'].unique())
    if 'category' in fund_master_df.columns:
        print("\nUnique Categories:\n", fund_master_df['category'].unique())
    if 'sub_category' in fund_master_df.columns:
        print("\nUnique Sub-Categories:\n", fund_master_df['sub_category'].unique())
    if 'risk_category' in fund_master_df.columns:
        print("\nUnique Risk Grades:\n", fund_master_df['risk_category'].unique())
    elif 'risk_grade' in fund_master_df.columns:
        print("\nUnique Risk Grades:\n", fund_master_df['risk_grade'].unique())
        
    print("\nAMFI Scheme Code Structure Understanding:")
    print("AMFI codes are unique numeric identifiers assigned to each mutual fund scheme by the Association of Mutual Funds in India.")

def validate_amfi_codes(fund_master_df, nav_history_df):
    print("\n--- Validating AMFI Codes ---")
    
    fm_code_col = 'amfi_code' if 'amfi_code' in fund_master_df.columns else 'scheme_code'
    nav_code_col = 'amfi_code' if 'amfi_code' in nav_history_df.columns else 'scheme_code'
    
    if fm_code_col not in fund_master_df.columns or nav_code_col not in nav_history_df.columns:
        print("Could not find the necessary column for AMFI code in datasets.")
        return

    fund_master_codes = set(fund_master_df[fm_code_col].dropna().unique())
    nav_history_codes = set(nav_history_df[nav_code_col].dropna().unique())
    
    valid_codes = fund_master_codes.intersection(nav_history_codes)
    invalid_codes = fund_master_codes - nav_history_codes
    
    print("Data Quality Summary:")
    print(f"Total unique codes in fund_master: {len(fund_master_codes)}")
    print(f"Codes found in nav_history: {len(valid_codes)}")
    print(f"Codes missing from nav_history: {len(invalid_codes)}")
    
    if invalid_codes:
        print(f"Some AMFI codes are present in fund_master but missing in nav_history.")
        print(f"Example missing codes: {list(invalid_codes)[:5]}")
    else:
        print("All AMFI codes in fund_master successfully validated against nav_history datasets.")

def main():
    datasets = load_and_explore_datasets()
    
    if '01_fund_master.csv' in datasets:
        explore_fund_master(datasets['01_fund_master.csv'])
        
    if '01_fund_master.csv' in datasets and '02_nav_history.csv' in datasets:
        validate_amfi_codes(datasets['01_fund_master.csv'], datasets['02_nav_history.csv'])
    else:
        print("\nCould not find '01_fund_master.csv' or '02_nav_history.csv' to validate AMFI codes.")

if __name__ == "__main__":
    main()
