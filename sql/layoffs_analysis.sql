-- ============================================================
-- Tech Layoffs Analysis — SQL Queries (2020–2024)
-- Database: tech_layoffs  |  Table: layoffs
-- Author: Tasnem Promy
-- ============================================================

-- ── Table Schema ─────────────────────────────────────────────
-- CREATE TABLE layoffs (
--     company          TEXT,
--     industry         TEXT,
--     country          TEXT,
--     year             INTEGER,
--     month            INTEGER,
--     stage            TEXT,
--     company_size     INTEGER,
--     layoffs_count    INTEGER,
--     layoffs_pct      REAL,
--     funds_raised_m   REAL,
--     reason           TEXT,
--     stock_impact_pct REAL,
--     severity         TEXT
-- );


-- ── 1. Total Layoffs per Year ─────────────────────────────────
SELECT
    year,
    SUM(layoffs_count)                          AS total_layoffs,
    COUNT(DISTINCT company)                      AS companies_affected,
    ROUND(AVG(layoffs_pct) * 100, 2)            AS avg_layoff_pct
FROM layoffs
GROUP BY year
ORDER BY year;


-- ── 2. Top 10 Industries by Total Layoffs ────────────────────
SELECT
    industry,
    SUM(layoffs_count)                          AS total_layoffs,
    ROUND(AVG(layoffs_pct) * 100, 2)            AS avg_pct_laid_off,
    COUNT(*)                                     AS layoff_events
FROM layoffs
GROUP BY industry
ORDER BY total_layoffs DESC
LIMIT 10;


-- ── 3. Companies with Largest Single Layoff Events ───────────
SELECT
    company,
    year,
    month,
    layoffs_count,
    ROUND(layoffs_pct * 100, 1)                 AS pct_laid_off,
    reason,
    severity
FROM layoffs
ORDER BY layoffs_count DESC
LIMIT 15;


-- ── 4. Layoff Severity Distribution by Funding Stage ─────────
SELECT
    stage,
    severity,
    COUNT(*)                                     AS event_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY stage), 1) AS pct_within_stage
FROM layoffs
GROUP BY stage, severity
ORDER BY stage, pct_within_stage DESC;


-- ── 5. Average Stock Impact by Industry (Public Companies) ───
SELECT
    industry,
    ROUND(AVG(stock_impact_pct), 2)             AS avg_stock_change_pct,
    COUNT(*)                                     AS public_events
FROM layoffs
WHERE stock_impact_pct IS NOT NULL
GROUP BY industry
HAVING COUNT(*) >= 5
ORDER BY avg_stock_change_pct ASC;


-- ── 6. Monthly Seasonality — Which Months See Most Layoffs ───
SELECT
    month,
    CASE month
        WHEN 1  THEN 'January'   WHEN 2  THEN 'February'
        WHEN 3  THEN 'March'     WHEN 4  THEN 'April'
        WHEN 5  THEN 'May'       WHEN 6  THEN 'June'
        WHEN 7  THEN 'July'      WHEN 8  THEN 'August'
        WHEN 9  THEN 'September' WHEN 10 THEN 'October'
        WHEN 11 THEN 'November'  WHEN 12 THEN 'December'
    END                                          AS month_name,
    SUM(layoffs_count)                           AS total_layoffs,
    COUNT(*)                                     AS events
FROM layoffs
GROUP BY month
ORDER BY total_layoffs DESC;


-- ── 7. Year-over-Year Growth in Layoffs ─────────────────────
WITH yearly AS (
    SELECT year, SUM(layoffs_count) AS total
    FROM layoffs
    GROUP BY year
)
SELECT
    year,
    total                                        AS layoffs,
    LAG(total) OVER (ORDER BY year)              AS prev_year,
    ROUND(
        (total - LAG(total) OVER (ORDER BY year)) * 100.0
        / NULLIF(LAG(total) OVER (ORDER BY year), 0), 1
    )                                            AS yoy_growth_pct
FROM yearly
ORDER BY year;


-- ── 8. Countries Most Affected (Layoffs per 1000 Employees) ──
SELECT
    country,
    SUM(layoffs_count)                           AS total_layoffs,
    SUM(company_size)                            AS total_employees,
    ROUND(SUM(layoffs_count) * 1000.0 / SUM(company_size), 2) AS layoffs_per_1000
FROM layoffs
GROUP BY country
ORDER BY layoffs_per_1000 DESC;


-- ── 9. High-Severity Layoffs — Detail View ───────────────────
SELECT
    company,
    industry,
    country,
    year,
    layoffs_count,
    ROUND(layoffs_pct * 100, 1)                 AS pct_laid_off,
    funds_raised_m,
    reason,
    COALESCE(ROUND(stock_impact_pct, 2)::TEXT, 'N/A') AS stock_impact
FROM layoffs
WHERE severity = 'High'
ORDER BY layoffs_count DESC
LIMIT 20;


-- ── 10. Layoffs vs Funds Raised Correlation Check ────────────
SELECT
    CASE
        WHEN funds_raised_m < 100    THEN '< $100M'
        WHEN funds_raised_m < 500    THEN '$100M–$500M'
        WHEN funds_raised_m < 1000   THEN '$500M–$1B'
        WHEN funds_raised_m < 5000   THEN '$1B–$5B'
        ELSE '$5B+'
    END                                          AS funding_bucket,
    COUNT(*)                                     AS events,
    ROUND(AVG(layoffs_pct) * 100, 2)            AS avg_layoff_pct,
    ROUND(AVG(layoffs_count), 0)                 AS avg_layoffs_count
FROM layoffs
GROUP BY funding_bucket
ORDER BY avg_layoff_pct DESC;
