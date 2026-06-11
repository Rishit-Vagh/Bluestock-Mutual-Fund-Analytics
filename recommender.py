"""
Module to recommend top mutual funds based on a given risk appetite.
"""
import sqlite3
import pandas as pd
import argparse

def recommend_funds(risk_appetite):
    """
    Query the database and print the top 3 recommended funds based on risk appetite.
    
    Args:
        risk_appetite (str): The user's risk appetite ('Low', 'Moderate', 'High').
    """
    risk_appetite = risk_appetite.capitalize()
    risk_mapping = {
        'Low': ['Low', 'Low to Moderate'],
        'Moderate': ['Moderate', 'Moderately High'],
        'High': ['High', 'Very High']
    }
    
    if risk_appetite not in risk_mapping:
        print("Invalid risk appetite. Choose Low, Moderate, or High.")
        return
        
    allowed_grades = risk_mapping[risk_appetite]
    
    conn = sqlite3.connect('bluestock_mf.db')
    
    query = f"""
        SELECT amfi_code, scheme_name, risk_grade, sharpe_ratio, return_3yr_pct
        FROM fact_performance
        WHERE risk_grade IN ({','.join(['?']*len(allowed_grades))})
        ORDER BY sharpe_ratio DESC
        LIMIT 3
    """
    
    df = pd.read_sql(query, conn, params=allowed_grades)
    conn.close()
    
    print(f"\nTop 3 Recommended Funds for '{risk_appetite}' Risk Appetite:")
    print("-" * 60)
    if df.empty:
        print("No funds found for this risk grade.")
    else:
        for index, row in df.iterrows():
            print(f"{index+1}. {row['scheme_name']}")
            print(f"   Risk Grade: {row['risk_grade']}")
            print(f"   Sharpe Ratio: {row['sharpe_ratio']:.2f}")
            print(f"   3-Year Return: {row['return_3yr_pct']:.2f}%\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fund Recommender based on Risk Appetite")
    parser.add_argument("risk", type=str, choices=["Low", "Moderate", "High", "low", "moderate", "high"], help="Risk appetite (Low/Moderate/High)")
    
    args = parser.parse_args()
    recommend_funds(args.risk)
