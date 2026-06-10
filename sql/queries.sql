

SELECT ticker, EXTRACT(MONTH FROM `date`) AS 'month', EXTRACT(YEAR FROM `date`) AS 'year', AVG(high - low) AS 'monthly range'
FROM daily_prices
GROUP BY ticker, `month`, `year`;

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

SELECT * FROM monthly_summary LIMIT 10;

SELECT * FROM regression_results;