# Project Changes Log

Note: all code, SQL, and implementation decisions in this project are mine. This doc is just me keeping track of what changed and why as I go, so I can reference it later (README, interviews, etc).

---

## 1. Domain pivot: AWS/Google Cloud/Oracle to EQIX/DLR/IRM
**Change:** Switched from analyzing AWS, Google Cloud, and Oracle to Equinix, Digital Realty, and Iron Mountain.
**Why:** AWS and Google Cloud are divisions of larger companies. Their stock prices reflect the performance of the entire parent company, not just datacenter operations. That's a construct validity problem, so I pivoted to pure play datacenter REITs instead.

---

## 2. Database: SQLite to MySQL
**Change:** Used MySQL Community Server instead of SQLite (which I used in Project 1).
**Why:** MySQL is a full server based relational database, more representative of a production environment, and needed for connecting Power BI and Excel via ODBC.

---

## 3. Regression dependent variable: daily_return to adjusted_close
**Change:** The growth regression was originally going to use daily_return as the dependent variable, with time as the independent variable. Switched to using adjusted_close as the dependent variable.
**Why:** Daily returns are small, noisy values that fluctuate around zero. A regression of daily returns against time mostly came back non-significant because there's no real trend in day to day returns for stable stocks. Adjusted close against time directly captures price growth over time, which is what "growth" actually means here.

---

## 4. Time variable: uncentered to centered
**Change:** Centered the time variable (time minus mean of time) before using it in the regression.
**Why:** With centering, the intercept becomes interpretable as the mean adjusted close price over the period, instead of a meaningless extrapolation to "day 0" before the data even starts. I verified empirically that the centered intercept equals the mean of adjusted_close.

---

## 5. Inferential statistics: Kruskal-Wallis and Dunn's test removed
**Change:** Ran Kruskal-Wallis and Dunn's post hoc tests (for stability via CV and growth via daily returns), then commented them out and excluded them from the final analysis.
**Why:** Daily stock prices are autocorrelated, today's price is influenced by yesterday's. That violates the independence of observations assumption these tests rely on (and regression p-values/standard errors too). With that assumption violated, the p-values aren't trustworthy and shouldn't be reported. The code is still there, commented out, as a record of what I tried and why I set it aside. The analysis is now purely descriptive: CV, regression slope, R squared, monthly return.

---

## 6. Stability Kruskal-Wallis: raw daily range to CV of daily range
**Change:** Before getting removed entirely (see #5), the stability Kruskal-Wallis was first run on raw daily price ranges (high minus low), then corrected to use CV of daily range instead.
**Why:** Raw daily ranges aren't comparable across companies trading at very different price levels (EQIX around $900 vs IRM around $100). CV normalizes for price level, same reasoning as why I used CV as the stability metric in the first place.

---

## 7. regression_results: separate table
**Change:** Regression outputs (slope, R squared, intercept, p-values) were originally going to live in monthly_summary, but I made a separate regression_results table instead.
**Why:** The regression uses all daily observations across the full year per company, so it's an annual per company result, not a monthly one. Putting it in monthly_summary would mean repeating the same value 13 times per company, which breaks normalization.

---

## 8. daily_return: moved from analysis notebook to ingestion notebook
**Change:** daily_return was originally calculated in 02_analysis.ipynb. Moved it to 01_data_ingestion.ipynb and stored it as a column in daily_prices.
**Why:** Power BI and Excel both need daily_return for drill down (pivot tables, charts). Calculating it at ingestion means downstream tools don't have to recalculate it, and it's available wherever daily_prices is used.

---

## 9. monthly_summary: added a real date column
**Change:** Added a date column (first day of each month, like 2025-06-01) to monthly_summary, populated with STR_TO_DATE(CONCAT(year, '-', month, '-01')).
**Why:** The old month column was just an integer 1 through 12 with no year attached. Power BI's date hierarchy couldn't tell June 2025 apart from June 2026, so charts grouped all the "Junes" together and showed up out of order. A real date column fixed it.

---

## 10. Power BI: removed the monthly return chart
**Change:** Added a chart showing average monthly_return by month and company, then removed it.
**Why:** It was redundant. daily_return is already in daily_prices and drillable up to monthly/quarterly/yearly in the Excel pivot table and date hierarchy. Having the same info in two places, calculated two different ways (monthly_return = (last_close minus first_close)/first_close vs average of daily returns), was just confusing.

---

## 11. Excel pivot table: removed daily_return
**Change:** Added daily_return to the Excel pivot table, then removed it.
**Why:** At quarterly/yearly level, average daily return is a tiny number (like -6.21667E-05) and shows up in scientific notation. Not meaningful at that level. Average adjusted close and sum of volume tell a clearer story.

---

## 12. Project framing: equity analysis to data engineering/pipeline demo
**Change:** Reframed the project from "rigorous equity analysis of REIT stability and growth" to "data engineering and BI pipeline demo using stock data as the domain."
**Why:** The metrics I used (CV of daily range, regression of price on time) aren't how real equity analysts assess REITs, they'd use beta, Sharpe ratio, drawdown, benchmark comparison. Rather than overstate the analytical rigor, I'm framing this honestly as showing ETL, relational database design, SQL, and BI dashboard skills. "Doing the analysis properly" is for Project 3 once I've built the domain knowledge on purpose.

---

## 13. Live data: Power BI streaming model to standalone real time component
**Change:** The plan for a real time price page was originally a Power BI Push/Streaming semantic model (via REST API, with Historic Data Analysis on), fed by a Python script.
**Why:** That requires a Power BI Service account (app.powerbi.com), which is tied to my university Microsoft 365 license and is gone now that I graduated. Checked, and a free Power BI Service account and Microsoft Fabric access are both unavailable without that license. Power Automate alone doesn't fix it either, since there's nowhere to push the data without a semantic model existing in Power BI Service to begin with.

Real time price is non negotiable for me, so the plan now is a standalone real time display, separate from the Power BI report: a local HTML/JS page connected to a WebSocket served by a Python script using yfinance's AsyncWebSocket, showing live current price, high, and low for EQIX, DLR, and IRM. I'll document the original Power BI intent (Push semantic model via REST API) in the README/methodology, along with why it couldn't happen as planned.

---

## 14. live_prices: two separate write operations instead of one
**Change:** live_prices (ticker, current_price, current_high, current_low, last_updated) gets written to by two separate, independently scheduled pieces, not one combined update per row.
**Why:** current_price comes from the WebSocket, which pushes updates whenever the price changes, no fixed interval. current_high/current_low come from a separate yf.download(ticker, period="1d") call on a 10 minute timer, since the day's high/low changes way less often than the live price. Combining these into one write would mean waiting on the slower one before either could update, which adds overhead for no reason. Writing them independently (UPDATE live_prices SET current_price = ... WHERE ticker = ... on each WebSocket message, and a separate UPDATE live_prices SET current_high = ..., current_low = ... WHERE ticker = ... every 10 minutes) lets each piece update on its own rhythm with minimal overhead.

---

## 15. live_prices: needs seed rows before UPDATE will do anything
**Change:** Found that the 10 minute high/low updater (UPDATE live_prices SET current_high = :high, current_low = :low WHERE ticker = :ticker) ran with no errors but wrote nothing, because live_prices had 0 rows.
**Why:** UPDATE ... WHERE only changes existing rows that match the condition. With 0 rows in live_prices, WHERE ticker = 'EQIX' matches nothing, so the UPDATE silently affects 0 rows. I need a one time seed step to insert the initial 3 rows (one per ticker, ticker filled in, everything else NULL) before the periodic UPDATE script can actually populate current_high/current_low (and later current_price via the WebSocket). This is a one time setup step, separate from the script that runs continuously.

---
