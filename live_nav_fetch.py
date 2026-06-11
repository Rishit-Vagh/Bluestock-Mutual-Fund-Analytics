"""
Module for fetching live NAV data from MFAPI.
"""
import requests
import pandas as pd
import os

def fetch_and_save_nav(scheme_code, scheme_name):
    """
    Fetch NAV data for a given scheme code and save it to a CSV file.
    
    Args:
        scheme_code (str): The AMFI scheme code.
        scheme_name (str): The name of the mutual fund scheme.
    """
    url = f"https://api.mfapi.in/mf/{scheme_code}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'data' in data:
            df = pd.DataFrame(data['data'])
            filename = f"data/raw/{scheme_name.replace(' ', '_').lower()}_{scheme_code}.csv"
            df.to_csv(filename, index=False)
            
if __name__ == "__main__":
    os.makedirs("data/raw", exist_ok=True)
    fetch_and_save_nav("125497", "HDFC Top 100 Direct")

    key_schemes = {
        "119551": "SBI Bluechip",
        "120503": "ICICI Bluechip",
        "118632": "Nippon Large Cap",
        "119092": "Axis Bluechip",
        "120841": "Kotak Bluechip"
    }

    for code, name in key_schemes.items():
        fetch_and_save_nav(code, name)
