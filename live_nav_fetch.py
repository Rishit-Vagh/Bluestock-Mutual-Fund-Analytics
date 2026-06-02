import requests
import pandas as pd
import os
import json

def fetch_and_save_nav(scheme_code, scheme_name):
    url = f"https://api.mfapi.in/mf/{scheme_code}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'data' in data:
            df = pd.DataFrame(data['data'])
            # The data contains 'date' and 'nav'
            # Save to data/raw
            filename = f"data/raw/{scheme_name.replace(' ', '_').lower()}_{scheme_code}.csv"
            df.to_csv(filename, index=False)
            print(f"Saved {scheme_name} NAV to {filename}")
        else:
            print(f"No 'data' found in response for {scheme_code}")
    else:
        print(f"Failed to fetch NAV for {scheme_code}: HTTP {response.status_code}")

if __name__ == "__main__":
    # Ensure directory exists
    os.makedirs("data/raw", exist_ok=True)

    # 1. Fetch HDFC Top 100 Direct
    fetch_and_save_nav("125497", "HDFC Top 100 Direct")

    # 2. Fetch 5 key schemes
    key_schemes = {
        "119551": "SBI Bluechip",
        "120503": "ICICI Bluechip",
        "118632": "Nippon Large Cap",
        "119092": "Axis Bluechip",
        "120841": "Kotak Bluechip"
    }

    for code, name in key_schemes.items():
        fetch_and_save_nav(code, name)
