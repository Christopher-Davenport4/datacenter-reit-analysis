-- ============================================================
-- SECTION 1: DATABASE SETUP
-- NOTE: All syntax was written by me. I had claude reorganize
-- it without changing any code
-- ============================================================

CREATE DATABASE IF NOT EXISTS datacenter_reits;
USE datacenter_reits;


-- ============================================================
-- SECTION 2: TABLE DEFINITIONS
-- Tables are created in dependency order (companies first,
-- since all other tables reference it via foreign key)
-- ============================================================

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
    `date` date,
    FOREIGN KEY (ticker)
	REFERENCES companies(ticker)
    );

-- p_value_slope and p_value_f were removed from regression_results.
-- the linear model is descriptive only. we are not trying to generalize
-- to a broader population, only characterize these three companies
-- over the trailing 12 month window. p values are not meaningful here.
CREATE TABLE IF NOT EXISTS regression_results (
	id INT AUTO_INCREMENT PRIMARY KEY,
	ticker varchar(15),
	regression_slope DECIMAL(10,6),
    r_squared DECIMAL(10,6),
    intercept DECIMAL(10,6),
	FOREIGN KEY (ticker)
	REFERENCES companies(ticker)
    );

-- live_prices stores the most recent intraday price data per company.
-- current_price is updated continuously via yfinance AsyncWebSocket.
-- current_high and current_low are updated every 10 minutes via yf.download(period='1d').
-- last_updated is set automatically by MySQL on each write.
CREATE TABLE IF NOT EXISTS live_prices (
	ticker varchar(15) PRIMARY KEY,
	current_price DECIMAL(10,3),
    current_high DECIMAL(10,3),
    current_low DECIMAL(10,3),
	last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (ticker)
    REFERENCES companies(ticker)
);


-- ============================================================
-- SECTION 3: SEED DATA
-- One-time inserts that do not change after initial setup
-- ============================================================

-- Seed live_prices with one row per ticker so UPDATE statements have rows to match against
INSERT INTO live_prices (ticker) VALUES ('DLR'), ('EQIX'), ('IRM');


-- ============================================================
-- REFERENCE: DROP STATEMENTS
-- Uncomment only if you need to fully reset the schema.
-- WARNING: this will delete all data in all tables.
-- ============================================================

-- DROP TABLE regression_results; 
-- DROP TABLE monthly_summary; 
-- DROP TABLE daily_prices; 
-- DROP TABLE companies;