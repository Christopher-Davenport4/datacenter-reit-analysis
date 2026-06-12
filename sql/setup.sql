CREATE DATABASE IF NOT EXISTS datacenter_reits;
SHOW DATABASES;


USE datacenter_reits;
-- DROP TABLE regression_results; 
-- DROP TABLE monthly_summary; 
-- DROP TABLE daily_prices; 
-- DROP TABLE companies; 



CREATE TABLE IF NOT EXISTS companies (
	ticker varchar(15) PRIMARY KEY,
    company_name varchar(255) NOT NULL,
    sector varchar(255), 
    exchange varchar(255)
    );

-- Auto Increment makes it so each id added is a unique number
CREATE TABLE IF NOT EXISTS daily_prices (
	id int AUTO_INCREMENT PRIMARY KEY,
    ticker varchar(15),
    `date` date,
    `open` DECIMAL(10,2),
     adjusted_close DECIMAL(10,2),
    high DECIMAL(10,2),
    low DECIMAL(10,2),
    volume bigint,
	daily_return DECIMAL(10,6),
    FOREIGN KEY (ticker)
    REFERENCES companies(ticker)
    );

  

CREATE TABLE IF NOT EXISTS monthly_summary (
	id int AUTO_INCREMENT PRIMARY KEY,
    ticker varchar(15),
    `year` int,
    `month` int, 
    mean_daily_range DECIMAL(10,4),
    sd_daily_range DECIMAL(10,4),
    cv_daily_range DECIMAL(10,4),
    mean_close DECIMAL(10,2),
    monthly_return DECIMAL(10,4),
    FOREIGN KEY (ticker)
	REFERENCES companies(ticker)
    );
ALTER TABLE monthly_summary 
    ADD `date` date;

-- DROP COLUMN r_squared;

CREATE TABLE IF NOT EXISTS regression_results (
	id INT AUTO_INCREMENT PRIMARY KEY,
	ticker varchar(15),
	regression_slope DECIMAL(10,6),
    r_squared DECIMAL(10,6),
    intercept DECIMAL (10,6),
  --   p_value_slope DECIMAL (10,6),
  --  p_value_f DECIMAL (10,6),
	FOREIGN KEY (ticker)
	REFERENCES companies(ticker)
    );
-- p values are dropped since we are not trying to generalize to a population
-- the linear model is descriptive in that we are only looking at these
-- companyes stability and growth. no broader trends are being looked at
-- ALTER TABLE regression_results
--  ADD COLUMN intercept DECIMAL (10,6),
-- DROP COLUMN p_value_slope,
-- DROP COLUMN p_value_f;


CREATE TABLE IF NOT EXISTS live_prices (
	ticker varchar(15) PRIMARY KEY,
	current_price DECIMAL(10,3),
    current_high DECIMAL(10,3),
    current_low DECIMAL(10,3),
	last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (ticker)
    REFERENCES companies(ticker)
);
INSERT INTO live_prices ( ticker, `year`, `month`, mean_close, mean_daily_range, sd_daily_range, cv_daily_range, monthly_return)
     -- SHOW TABLES;
     -- describe companies;
     -- describe daily_prices;
     -- describe monthly_summary; 


-- ALTER USER 'root'@'localhost' IDENTIFIED BY 'beans123';