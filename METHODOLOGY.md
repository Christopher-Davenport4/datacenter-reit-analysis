# Context

I wanted to do a project that utilized live data, and came to the conclusion that I wanted to track the performance of companies investing in AI data centers. Initially I was going to look at AWS, Google Cloud, and Oracle. My plan was to look at their respective growths over the past year, and the month-to-month stability of the stock price. Before moving on to operationalizing what growth or stability looked like, I started to question the construct validity of these companies. That is, AWS and Google Cloud are divisions of companies that are not solely connected to data centers. Their prices are going to be influenced by the performance of the larger companies and other extraneous factors. As a result, I decided to pivot and look at companies that work primarily in datacenter real estate. From here, I landed on Equinix (EQIX), Digital Realty (DLR), and Iron Mountain (IRM). However, Iron Mountain is a bit of an outlier as they started in physical document storage and have been transitioning into datacenters. As the medium is still primarily storage in a similar capacity, I figured this would offer interesting comparisons to be made between the three companies.

## Advantages of Comparing EQIX, DLR, and IRM

- These companies are in the same sector
- These companies have the same asset class
- These companies are going to receive the same sort of regulatory treatment
- These companies compete for similar customers
- These companies are influenced by similar external factors (e.g., energy costs, interest rates, land pricing)
- In sum, there is enough congruency between these companies such that the results ascertained from these analyses may help generate real world insight.

# Operationalization of Stability and Growth

## Stability

### Descriptive

In order to descriptively look at the stability of growth for each company, I am going to look at the fluctuation of daily stock prices using the range of the price (High - Low) aggregated to the month level. I am then going to compute the coefficient of variation for each month by computing the mean and standard deviation for the range, and dividing the standard deviation by the mean.

**Rationale:** Initially I wanted to look at daily volatility by working with real time data. However, I do not have the means to collect this type of data. As a result, I opted for the method described above. I did this for a couple of reasons:

The coefficient of variation (CV) is a metric that allows you to compare variability across different metrics. Comparing standard deviations by themselves is difficult and often invalid as metrics can have the same number but different meanings. For instance, a company worth on average $100 with a SD of $15 is much different than a company worth on average $1000 with an SD of $15. The former has 68% of the data falling within $75 and $115, while the latter is $985 to $1015. However, if we computed the CV, the former would be 15% while the latter is 1.5%.

## Growth

### Regression Analysis

In order to characterize each company's growth trajectory, I ran separate linear regressions with time (trading day) as the independent variable and adjusted close as the dependent variable. The slope indicates the rate of price growth over time, and R² indicates how consistently the company grew in that direction. A high R² means the stock followed a steady upward trend, while a low R² means growth was erratic even if the overall return was positive.

# Methodological Decisions and Limitations

## On Inferential Statistics

During the planning phase of this project, I considered running inferential tests to assess whether the stability and growth differences between companies were statistically significant. Specifically, I considered a Kruskal-Wallis test followed by Dunn's post-hoc comparisons for both stability (using CV) and growth (using daily returns).

After running these tests, I made the decision not to include them in the final analysis. The core issue is that daily stock prices are autocorrelated: today's price is influenced by yesterday's price, which violates the independence of observations assumption that underlies both the Kruskal-Wallis test and the standard errors of the linear regression. When this assumption is violated, p-values are not trustworthy and cannot be meaningfully interpreted.

This is not unique to this project. It is a known and well-documented challenge in financial time series analysis. The appropriate solution would be to model autocorrelation explicitly, for example using ARIMA-based methods or regression with autocorrelation-corrected standard errors. This is identified as a direction for future work.

As a result, this analysis is purely descriptive. The CV characterizes stability, and the regression slope and R² characterize growth rate and consistency. These metrics directly answer the research question without requiring the independence assumption.

The inferential test code remains in the analysis notebook, commented out, as a record of what was attempted and why it was set aside.

## Independence of Observations

This assumption only partially holds. While observations across companies are independent from one another, daily stock prices within each company are not fully independent as previous prices influence current prices. This is known as autocorrelation and is a well-documented property of time series data.

## Normality of Residuals (Linear Regression)

Linear regression assumes that the residuals are approximately normally distributed, not the raw data itself. Following each regression, residual plots will be inspected to assess whether this assumption holds. Any meaningful violations will be noted as a limitation.

## Data Source and Time Window

All data will be sourced from yfinance over a trailing 12-month window. Adjusted close prices will be used rather than raw close prices to account for stock splits and dividends, which would otherwise introduce artificial distortions in the price series.

## Aggregation Period

The default aggregation period for stability metrics is monthly, consistent with the research question. The pipeline is parameterized to support weekly aggregation without changes to the underlying code.
