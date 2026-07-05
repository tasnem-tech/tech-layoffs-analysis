"""
generate_data.py
Generates a realistic synthetic Tech Layoffs dataset (2020–2024)
and saves it to data/tech_layoffs.csv
"""

import pandas as pd
import numpy as np
import os

np.random.seed(42)
N = 1500

companies = [
    "Meta", "Amazon", "Google", "Microsoft", "Twitter/X", "Salesforce",
    "Spotify", "Lyft", "Stripe", "Snap", "Cisco", "Intel", "Dell",
    "HP", "IBM", "SAP", "Oracle", "Airbnb", "Uber", "Netflix",
    "Zoom", "Shopify", "Dropbox", "LinkedIn", "PayPal", "eBay",
    "Robinhood", "Coinbase", "Unity", "Twilio", "Peloton", "Wayfair",
    "Better.com", "Opendoor", "Klarna", "Bolt", "Gorillas", "Getir",
]

industries = ["Social Media", "E-Commerce", "Cloud Computing", "FinTech",
               "EdTech", "HealthTech", "Gaming", "Cybersecurity",
               "AI/ML", "Logistics", "SaaS", "Hardware"]

stages = ["Public", "Series D+", "Series C", "Series B", "Series A", "Private Equity"]
countries = ["USA", "UK", "Germany", "India", "Canada", "Australia",
             "France", "Netherlands", "Singapore", "Brazil"]

company_col = np.random.choice(companies, N)
industry_col = np.random.choice(industries, N)
year_col = np.random.choice([2020, 2021, 2022, 2023, 2024], N,
                             p=[0.08, 0.07, 0.30, 0.35, 0.20])
month_col = np.random.randint(1, 13, N)
stage_col = np.random.choice(stages, N, p=[0.35, 0.20, 0.18, 0.12, 0.08, 0.07])
country_col = np.random.choice(countries, N, p=[0.45, 0.10, 0.08, 0.08,
                                                  0.07, 0.05, 0.05, 0.04, 0.04, 0.04])

# Company size correlates with layoffs count
company_size = np.random.randint(500, 150000, N)
layoffs_pct = np.clip(np.random.normal(0.12, 0.08, N), 0.01, 0.80)
layoffs_count = (company_size * layoffs_pct).astype(int)

# Funds raised (millions USD) — higher for later stages
funds_map = {"Public": 5000, "Series D+": 800, "Series C": 300,
             "Series B": 120, "Series A": 40, "Private Equity": 1500}
base_funds = np.array([funds_map[s] for s in stage_col])
funds_raised = np.abs(np.random.normal(base_funds, base_funds * 0.4)).round(1)

# Sentiment-encoded reason
reasons = ["Cost Cutting", "Restructuring", "Over-hiring Post-COVID",
           "Market Downturn", "Product Pivot", "Merger/Acquisition",
           "IPO Preparation", "Regulatory Pressure"]
reason_col = np.random.choice(reasons, N)

# Stock impact (% change around layoff announcement) — public only
stock_impact = np.where(
    stage_col == "Public",
    np.random.normal(-3.5, 5.0, N).round(2),
    np.nan
)

# Severity label (target for ML)
def severity(pct):
    if pct < 0.05:
        return "Low"
    elif pct < 0.15:
        return "Medium"
    else:
        return "High"

severity_col = [severity(p) for p in layoffs_pct]

df = pd.DataFrame({
    "company": company_col,
    "industry": industry_col,
    "country": country_col,
    "year": year_col,
    "month": month_col,
    "stage": stage_col,
    "company_size": company_size,
    "layoffs_count": layoffs_count,
    "layoffs_pct": layoffs_pct.round(4),
    "funds_raised_m": funds_raised,
    "reason": reason_col,
    "stock_impact_pct": stock_impact,
    "severity": severity_col,
})

os.makedirs("data", exist_ok=True)
df.to_csv("data/tech_layoffs.csv", index=False)
print(f"Dataset saved: {df.shape[0]} rows, {df.shape[1]} columns")
print(df.head())
