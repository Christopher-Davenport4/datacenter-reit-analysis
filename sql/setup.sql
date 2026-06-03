CREATE DATABASE IF NOT EXISTS datacenter_reits;
SHOW DATABASES;

-- Auto Increment makes it so each id added is a unique number
USE datacenter_reits;
DROP TABLE monthly_summary; 
DROP TABLE daily_prices; 
DROP TABLE companies; 



CREATE TABLE IF NOT EXISTS companies (
	ticker varchar(15) PRIMARY KEY,
    company_name varchar(255) NOT NULL,
    sector varchar(255), 
    exchange varchar(255)
    );

CREATE TABLE IF NOT EXISTS daily_prices (
	id int AUTO_INCREMENT PRIMARY KEY,
    ticker varchar(15),
    `date` date,
    open DECIMAL(10,2),
    close DECIMAL(10,2),
    high DECIMAL(10,2),
    low DECIMAL(10,2),
    volume bigint,
    adjusted_close DECIMAL(10,2),
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
    regression_slope DECIMAL(10,6),
    r_squared DECIMAL(10,6),
    monthly_return DECIMAL(10,4),
    FOREIGN KEY (ticker)
	REFERENCES companies(ticker)
    );
    
    
    SHOW TABLES;
     -- describe companies;
     -- describe daily_prices;
     describe monthly_summary; 