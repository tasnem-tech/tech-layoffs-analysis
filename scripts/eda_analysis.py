"""
eda_analysis.py
Exploratory Data Analysis of Tech Layoffs (2020–2024)
Generates all charts saved to visuals/
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns
import warnings
import os

warnings.filterwarnings("ignore")
os.makedirs("visuals", exist_ok=True)

# ── Styling ──────────────────────────────────────────────────────────────────
PALETTE = ["#1f4e79", "#2e75b6", "#4da6d9", "#a9d6f5", "#d9e8f5"]
sns.set_theme(style="whitegrid", font_scale=1.1)
plt.rcParams.update({
    "figure.dpi": 150,
    "font.family": "DejaVu Sans",
    "axes.spines.top": False,
    "axes.spines.right": False,
})

# ── Load Data ─────────────────────────────────────────────────────────────────
df = pd.read_csv("data/tech_layoffs.csv")
print(f"Shape: {df.shape}")
print(df.dtypes)
print("\nMissing values:\n", df.isnull().sum())
print("\nBasic stats:\n", df.describe())

# ── 1. Layoffs by Year ────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(9, 5))
yearly = df.groupby("year")["layoffs_count"].sum().reset_index()
bars = ax.bar(yearly["year"].astype(str), yearly["layoffs_count"] / 1000,
              color=PALETTE[0], edgecolor="white", linewidth=0.8)
ax.bar_label(bars, labels=[f"{v:.1f}k" for v in yearly["layoffs_count"] / 1000],
             padding=4, fontsize=10, color="#1f4e79", fontweight="bold")
ax.set_title("Total Tech Layoffs by Year (2020–2024)", fontsize=14, fontweight="bold", pad=12)
ax.set_xlabel("Year")
ax.set_ylabel("Layoffs (thousands)")
ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"{x:.0f}k"))
plt.tight_layout()
plt.savefig("visuals/01_layoffs_by_year.png")
plt.close()
print("Saved: 01_layoffs_by_year.png")

# ── 2. Layoffs by Industry ────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 6))
ind_data = (df.groupby("industry")["layoffs_count"]
              .sum()
              .sort_values(ascending=True))
colors = sns.color_palette("Blues_d", len(ind_data))
bars = ax.barh(ind_data.index, ind_data.values / 1000, color=colors)
ax.bar_label(bars, labels=[f"{v:.1f}k" for v in ind_data.values / 1000],
             padding=3, fontsize=9)
ax.set_title("Total Layoffs by Industry", fontsize=14, fontweight="bold", pad=12)
ax.set_xlabel("Layoffs (thousands)")
plt.tight_layout()
plt.savefig("visuals/02_layoffs_by_industry.png")
plt.close()
print("Saved: 02_layoffs_by_industry.png")

# ── 3. Top 10 Companies by Layoffs ───────────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 5))
top10 = (df.groupby("company")["layoffs_count"]
           .sum()
           .sort_values(ascending=False)
           .head(10))
colors2 = ["#1f4e79" if i == 0 else "#2e75b6" if i < 3 else "#4da6d9"
           for i in range(len(top10))]
bars = ax.bar(top10.index, top10.values / 1000, color=colors2, edgecolor="white")
ax.bar_label(bars, labels=[f"{v:.1f}k" for v in top10.values / 1000],
             padding=3, fontsize=9, fontweight="bold")
ax.set_title("Top 10 Companies by Total Layoffs", fontsize=14, fontweight="bold", pad=12)
ax.set_xlabel("Company")
ax.set_ylabel("Layoffs (thousands)")
plt.xticks(rotation=30, ha="right")
plt.tight_layout()
plt.savefig("visuals/03_top10_companies.png")
plt.close()
print("Saved: 03_top10_companies.png")

# ── 4. Layoff Severity Distribution ──────────────────────────────────────────
fig, ax = plt.subplots(figsize=(7, 5))
sev_counts = df["severity"].value_counts()
wedge_props = {"linewidth": 2, "edgecolor": "white"}
ax.pie(sev_counts, labels=sev_counts.index,
       autopct="%1.1f%%", colors=["#4da6d9", "#1f4e79", "#f4b942"],
       wedgeprops=wedge_props, startangle=140,
       textprops={"fontsize": 11})
ax.set_title("Layoff Severity Distribution", fontsize=14, fontweight="bold", pad=12)
plt.tight_layout()
plt.savefig("visuals/04_severity_distribution.png")
plt.close()
print("Saved: 04_severity_distribution.png")

# ── 5. Monthly Trend Heatmap ──────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(12, 5))
pivot = df.pivot_table(values="layoffs_count", index="year",
                        columns="month", aggfunc="sum", fill_value=0)
pivot.columns = ["Jan","Feb","Mar","Apr","May","Jun",
                 "Jul","Aug","Sep","Oct","Nov","Dec"]
sns.heatmap(pivot / 1000, annot=True, fmt=".1f", cmap="Blues",
            linewidths=0.5, ax=ax, cbar_kws={"label": "Layoffs (k)"})
ax.set_title("Layoffs Heatmap: Year × Month (thousands)", fontsize=13,
             fontweight="bold", pad=12)
ax.set_xlabel("Month")
ax.set_ylabel("Year")
plt.tight_layout()
plt.savefig("visuals/05_monthly_heatmap.png")
plt.close()
print("Saved: 05_monthly_heatmap.png")

# ── 6. Layoffs % by Funding Stage ────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(9, 5))
stage_pct = df.groupby("stage")["layoffs_pct"].median().sort_values(ascending=False)
bars = ax.bar(stage_pct.index, stage_pct.values * 100,
              color=sns.color_palette("Blues_d", len(stage_pct)))
ax.bar_label(bars, labels=[f"{v:.1f}%" for v in stage_pct.values * 100],
             padding=3, fontsize=9, fontweight="bold")
ax.set_title("Median Layoff % by Funding Stage", fontsize=14, fontweight="bold", pad=12)
ax.set_xlabel("Funding Stage")
ax.set_ylabel("Median Layoff %")
ax.yaxis.set_major_formatter(mtick.PercentFormatter())
plt.xticks(rotation=20)
plt.tight_layout()
plt.savefig("visuals/06_layoffs_by_stage.png")
plt.close()
print("Saved: 06_layoffs_by_stage.png")

# ── 7. Stock Impact Distribution ─────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(9, 5))
stock_df = df.dropna(subset=["stock_impact_pct"])
ax.hist(stock_df["stock_impact_pct"], bins=35, color="#2e75b6",
        edgecolor="white", linewidth=0.6)
ax.axvline(stock_df["stock_impact_pct"].mean(), color="#f4b942",
           linestyle="--", linewidth=1.8,
           label=f"Mean: {stock_df['stock_impact_pct'].mean():.2f}%")
ax.set_title("Stock Price Impact at Layoff Announcement (Public Companies)",
             fontsize=13, fontweight="bold", pad=12)
ax.set_xlabel("Stock Change %")
ax.set_ylabel("Frequency")
ax.legend()
plt.tight_layout()
plt.savefig("visuals/07_stock_impact.png")
plt.close()
print("Saved: 07_stock_impact.png")

# ── 8. Country Distribution ───────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(9, 5))
country_data = (df.groupby("country")["layoffs_count"]
                  .sum()
                  .sort_values(ascending=False))
bars = ax.bar(country_data.index, country_data.values / 1000,
              color=PALETTE[1], edgecolor="white")
ax.bar_label(bars, labels=[f"{v:.0f}k" for v in country_data.values / 1000],
             padding=3, fontsize=9)
ax.set_title("Total Layoffs by Country", fontsize=14, fontweight="bold", pad=12)
ax.set_xlabel("Country")
ax.set_ylabel("Layoffs (thousands)")
plt.xticks(rotation=30, ha="right")
plt.tight_layout()
plt.savefig("visuals/08_layoffs_by_country.png")
plt.close()
print("Saved: 08_layoffs_by_country.png")

# ── 9. Correlation Heatmap ────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(7, 6))
num_cols = ["company_size", "layoffs_count", "layoffs_pct",
            "funds_raised_m", "stock_impact_pct"]
corr = df[num_cols].corr()
mask = np.triu(np.ones_like(corr, dtype=bool))
sns.heatmap(corr, mask=mask, annot=True, fmt=".2f", cmap="coolwarm",
            center=0, linewidths=0.5, ax=ax,
            cbar_kws={"shrink": 0.8})
ax.set_title("Correlation Matrix — Numerical Features",
             fontsize=13, fontweight="bold", pad=12)
plt.tight_layout()
plt.savefig("visuals/09_correlation_heatmap.png")
plt.close()
print("Saved: 09_correlation_heatmap.png")

# ── 10. Layoff Reason Breakdown ───────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 5))
reason_data = df["reason"].value_counts()
colors3 = sns.color_palette("Blues_d", len(reason_data))
bars = ax.barh(reason_data.index, reason_data.values, color=colors3)
ax.bar_label(bars, padding=3, fontsize=9)
ax.set_title("Layoff Events by Stated Reason", fontsize=14, fontweight="bold", pad=12)
ax.set_xlabel("Number of Layoff Events")
plt.tight_layout()
plt.savefig("visuals/10_layoff_reasons.png")
plt.close()
print("Saved: 10_layoff_reasons.png")

print("\nAll 10 visualisations saved to visuals/")
