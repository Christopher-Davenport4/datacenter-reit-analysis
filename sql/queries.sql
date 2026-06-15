-- ============================================================
-- SECTION 1: PIPELINE QUERIES
-- These queries are run via Python (02_analysis.ipynb) as part
-- of the ETL pipeline. They are documented here for reference.
-- NOTE: All syntax was written by me. I had claude reorganize
-- it without changing any code
-- ============================================================
 
-- Step 1: Exploratory check of average daily range by month (used during development)
SELECT ticker, EXTRACT(MONTH FROM `date`) AS 'month', EXTRACT(YEAR FROM `date`) AS 'year', AVG(high - low) AS 'monthly range'
FROM daily_prices
GROUP BY ticker, `month`, `year`;
 
-- Step 2: Clear monthly_summary before repopulating (prevents duplicates on reruns)
TRUNCATE TABLE monthly_summary;
 
-- Step 3: Populate monthly_summary using CTEs and window functions
-- Uses FIRST_VALUE and LAST_VALUE to capture opening and closing prices per month
-- Calculates mean daily range, standard deviation, CV, and monthly return
INSERT INTO monthly_summary ( ticker, `year`, `month`, mean_close, mean_daily_range, sd_daily_range, cv_daily_range, monthly_return)
WITH base AS (
	SELECT ticker, 
		EXTRACT(MONTH FROM `date`) AS 'month', 
		EXTRACT(YEAR FROM `date`) AS 'year', 
		(high - low) AS 'daily range',
        `adjusted_close`,
        	FIRST_VALUE(adjusted_close) OVER (PARTITION BY ticker, EXTRACT(MONTH FROM `date`), EXTRACT(YEAR FROM `date`) ORDER BY `date`) AS first_close,
			LAST_VALUE(adjusted_close) OVER (PARTITION BY ticker, EXTRACT(MONTH FROM `date`), EXTRACT(YEAR FROM `date`) ORDER BY `date`  ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS last_close
FROM daily_prices
),
monthly_stats AS (
	SELECT `ticker`, `month`, `year`,
    AVG(`adjusted_close`) AS 'mean_close',
    AVG(`daily range`) AS 'mean_daily_range',
	STDDEV_SAMP(`daily range`) as 'sd_daily_range',
    ANY_VALUE(first_close) AS first_close,
	ANY_VALUE(last_close) AS last_close
FROM base
GROUP BY ticker, `month`, `year`
)
SELECT ticker, `year`, `month`, mean_close, mean_daily_range, sd_daily_range,
	`sd_daily_range` / `mean_daily_range` AS 'cv_daily_range',
    (`last_close` - `first_close`) / `first_close` as 'monthly_return'
FROM monthly_stats;
 
-- Step 4: Populate the date column after insert
-- Constructs a proper DATE value from year and month integers for use in Power BI
UPDATE monthly_summary 
SET `date` = STR_TO_DATE(CONCAT(`year`, '-', `month`, '-01'), '%Y-%m-%d');
 
 
-- ============================================================
-- SECTION 2: ANALYTICAL QUERIES
-- Multi-table JOIN queries combining companies with fact tables
-- to produce readable, analyst-friendly output
-- ============================================================
 
/* the following JOIN syntax combines contents from the companies and daily_prices today by joining them together with the ticker key */
SELECT companies.company_name, daily_prices.date, daily_prices.adjusted_close, daily_prices.daily_return
FROM companies
JOIN daily_prices on companies.ticker = daily_prices.ticker;
 
SELECT companies.company_name, monthly_summary.year, monthly_summary.month, monthly_summary.mean_close, monthly_summary.cv_daily_range,  monthly_summary.monthly_return
FROM companies
JOIN monthly_summary on companies.ticker = monthly_summary.ticker;
 
/* In this context, LEFT JOIN will join the rows based the contents in companies. If there are rows that exist within companies, but not within monthly_summary,
the output will display null results to shed light on this descrepancy */
SELECT companies.company_name, daily_prices.date, daily_prices.adjusted_close, daily_prices.daily_return
FROM companies
LEFT JOIN daily_prices on companies.ticker = daily_prices.ticker;
 
SELECT companies.company_name, monthly_summary.year, monthly_summary.month, monthly_summary.mean_close, monthly_summary.cv_daily_range,  monthly_summary.monthly_return
FROM companies -- this is the left table
LEFT JOIN monthly_summary /*this is the right table*/  on companies.ticker = monthly_summary.ticker;
 
/* In this context, RIGHT JOIN will join the rows based the contents in daily_prices. If there are rows that exist within daily_prices, but not within companies,
the output will display null results to shed light on this descrepancy */
SELECT companies.company_name, daily_prices.date, daily_prices.adjusted_close, daily_prices.daily_return
FROM companies 
RIGHT JOIN daily_prices on companies.ticker = daily_prices.ticker;
 
SELECT companies.company_name, monthly_summary.year, monthly_summary.month, monthly_summary.mean_close, monthly_summary.cv_daily_range,  monthly_summary.monthly_return
FROM companies
RIGHT JOIN monthly_summary on companies.ticker = monthly_summary.ticker;
 