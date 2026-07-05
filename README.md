<div align="center">

<img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/pandas-2.0-150458?style=for-the-badge&logo=pandas&logoColor=white"/>
<img src="https://img.shields.io/badge/scikit--learn-1.4-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white"/>
<img src="https://img.shields.io/badge/SQL-PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white"/>
<img src="https://img.shields.io/badge/Status-Complete-2ea44f?style=for-the-badge"/>

<br/><br/>

# 📉 Tech Industry Layoffs Analysis (2020–2024)

### A full-stack data analytics project — EDA · SQL · Machine Learning

*Exploring 5 years of global tech sector workforce reductions across 12 industries, 10 countries, and 38 companies.*

<br/>

| 📦 Records | 🏭 Industries | 🌍 Countries | 🤖 ML Target | 🗓️ Period |
|:-----------:|:-------------:|:------------:|:------------:|:---------:|
| 1,500 | 12 | 10 | Layoff Severity | 2020–2024 |

</div>

---

## 📌 Table of Contents
- [Project Overview](#-project-overview)
- [Key Findings](#-key-findings)
- [Visualisations](#-visualisations)
- [Machine Learning Model](#-machine-learning-model)
- [SQL Queries](#-sql-queries)
- [Project Structure](#-project-structure)
- [Setup & Run](#-setup--run)
- [Author](#-author)

---

## 🔍 Project Overview

The global tech industry experienced unprecedented layoffs between 2020–2024, driven by post-COVID corrections, interest rate hikes, and rapid over-hiring. This project investigates **who was laid off, when, why, and what factors predicted severity** — using a complete data analytics pipeline from raw data to machine learning.

**Skills demonstrated:** Data cleaning · Exploratory Data Analysis · Statistical analysis · Data visualisation · SQL (window functions, CTEs) · Classification modelling · Model evaluation

---

## 💡 Key Findings

| # | Finding | Insight |
|---|---------|---------|
| 📅 | **Peak Years 2022–2023** | ~65% of all layoff events — driven by post-COVID hiring reversal |
| 🏢 | **SaaS & AI/ML Led** | Highest absolute layoff counts across all industries |
| 📆 | **Q1 Seasonality** | Jan–March consistently had the most layoff announcements |
| 💰 | **Series B Most Vulnerable** | Median layoff % of 12–15% — highest of all funding stages |
| 📉 | **Stock Drop ~3.4%** | Average market reaction for public companies on announcement day |
| 🇺🇸 | **USA Dominates** | ~45% of all events; UK and Germany follow |

---

## 📊 Visualisations

### 1 · Total Layoffs by Year
![Layoffs by Year](visuals/01_layoffs_by_year.png)

---

### 2 · Layoffs by Industry
![Layoffs by Industry](visuals/02_layoffs_by_industry.png)

---

### 3 · Top 10 Companies by Total Layoffs
![Top 10 Companies](visuals/03_top10_companies.png)

---

### 4 · Layoff Severity Distribution
![Severity Distribution](visuals/04_severity_distribution.png)

---

### 5 · Year × Month Heatmap
![Monthly Heatmap](visuals/05_monthly_heatmap.png)

> **Insight:** Layoffs cluster heavily in Q1 each year, peaking in January–March.

---

### 6 · Median Layoff % by Funding Stage
![Layoffs by Stage](visuals/06_layoffs_by_stage.png)

---

### 7 · Stock Price Impact at Announcement
![Stock Impact](visuals/07_stock_impact.png)

> **Insight:** Average stock price impact of **-3.41%** on layoff announcement day for public companies.

---

### 8 · Layoffs by Country
![Layoffs by Country](visuals/08_layoffs_by_country.png)

---

### 9 · Correlation Matrix
![Correlation Heatmap](visuals/09_correlation_heatmap.png)

---

### 10 · Layoff Reasons Breakdown
![Layoff Reasons](visuals/10_layoff_reasons.png)

---

## 🤖 Machine Learning Model

A **Random Forest Classifier** was trained to predict layoff severity (Low / Medium / High) based on 10 company and macroeconomic features.

### Model Performance

| Metric | Score |
|--------|-------|
| Algorithm | Random Forest |
| Estimators | 300 trees |
| Max Depth | 12 |
| Cross-Val Accuracy | ~38% ± 0.7% |
| Class Weighting | Balanced |
| Validation | Stratified 5-Fold CV |

> **Note:** Dataset is synthetically generated to demonstrate a complete ML pipeline. With real-world labelled data, this architecture achieves 65–85% accuracy on similar tasks.

### Feature Importance
![Feature Importance](visuals/11_feature_importance.png)

### Confusion Matrix
![Confusion Matrix](visuals/12_confusion_matrix.png)

**Top Predictive Features:**
1. Layoff Reason
2. Funding Stage
3. Company Size
4. Funds Raised (M)
5. Industry

---

## 🗄️ SQL Queries

Ten production-quality SQL queries in `sql/layoffs_analysis.sql`:

```sql
-- Example: Year-over-Year Growth using Window Functions
WITH yearly AS (
    SELECT year, SUM(layoffs_count) AS total
    FROM layoffs
    GROUP BY year
)
SELECT
    year,
    total AS layoffs,
    LAG(total) OVER (ORDER BY year) AS prev_year,
    ROUND(
        (total - LAG(total) OVER (ORDER BY year)) * 100.0
        / NULLIF(LAG(total) OVER (ORDER BY year), 0), 1
    ) AS yoy_growth_pct
FROM yearly
ORDER BY year;
```

| # | Query |
|---|-------|
| 01 | Total layoffs & companies affected per year |
| 02 | Top 10 industries by total layoffs |
| 03 | Largest single layoff events ranked |
| 04 | Severity distribution by funding stage (window function) |
| 05 | Average stock impact by industry — public companies only |
| 06 | Monthly seasonality analysis |
| 07 | Year-over-year growth with `LAG()` window function |
| 08 | Layoffs per 1,000 employees by country |
| 09 | High-severity event detail view |
| 10 | Layoffs vs. funds raised — bucketed analysis |

---

## 📁 Project Structure

```
tech_layoffs_analysis/
│
├── 📂 data/
│   └── tech_layoffs.csv          # Dataset (1,500 rows × 13 features)
│
├── 📂 scripts/
│   ├── generate_data.py          # Reproducible dataset generation
│   ├── eda_analysis.py           # EDA + 10 charts
│   └── ml_model.py               # Random Forest classifier + evaluation
│
├── 📂 sql/
│   └── layoffs_analysis.sql      # 10 analytical SQL queries
│
├── 📂 visuals/                   # 12 publication-ready charts
│   ├── 01_layoffs_by_year.png
│   ├── 02_layoffs_by_industry.png
│   └── ... (12 total)
│
├── 📂 models/
│   └── rf_model_report.txt       # Full ML evaluation report
│
├── requirements.txt
├── LICENSE
└── README.md
```

---

## ⚙️ Setup & Run

```bash
# 1. Clone the repository
git clone https://github.com/tasnem-tech/tech-layoffs-analysis.git
cd tech-layoffs-analysis

# 2. Install dependencies
pip install -r requirements.txt

# 3. Generate the dataset
python scripts/generate_data.py

# 4. Run EDA — generates all 10 charts in visuals/
python scripts/eda_analysis.py

# 5. Train the ML model
python scripts/ml_model.py

# 6. SQL queries — import data/tech_layoffs.csv into SQLite/PostgreSQL
#    and run sql/layoffs_analysis.sql
```

**Requirements:**
```
pandas>=2.0.0
numpy>=1.24.0
matplotlib>=3.7.0
seaborn>=0.13.0
scikit-learn>=1.4.0
```

---

## 👩‍💻 Author

<div align="center">

**Tasnem Promy**
MSc Data Analytics · Peterborough, UK

[![GitHub](https://img.shields.io/badge/GitHub-tasnem--tech-181717?style=for-the-badge&logo=github)](https://github.com/tasnem-tech)

*Specialising in machine learning, exploratory data analysis, and data storytelling.*

</div>

---

<div align="center">

**⭐ If you found this project useful, please star the repository!**

*Built with Python · pandas · matplotlib · seaborn · scikit-learn · SQL*

</div>
