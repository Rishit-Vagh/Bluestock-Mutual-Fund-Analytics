"""
Master execution script for the Bluestock MF Capstone ETL pipeline.
Runs data fetching, ingestion, cleaning, and DB loading sequentially.
"""
import os
import live_nav_fetch
import data_ingestion
import process_data

def main():
    print("Starting ETL Pipeline...")
    
    print("\n1. Fetching Live NAV Data...")
    os.makedirs("data/raw", exist_ok=True)
    live_nav_fetch.fetch_and_save_nav("125497", "HDFC Top 100 Direct")
    key_schemes = {
        "119551": "SBI Bluechip",
        "120503": "ICICI Bluechip",
        "118632": "Nippon Large Cap",
        "119092": "Axis Bluechip",
        "120841": "Kotak Bluechip"
    }
    for code, name in key_schemes.items():
        live_nav_fetch.fetch_and_save_nav(code, name)
        
    print("\n2. Ingesting and Exploring Data...")
    data_ingestion.main()
    
    print("\n3. Processing Data and Loading to SQLite...")
    process_data.clean_data()
    process_data.generate_dim_date()
    process_data.load_to_sqlite()
    
    print("\nETL Pipeline Completed Successfully!")

if __name__ == "__main__":
    main()
