#Context

I wanted to do a project that utilized live data, and came to the conclusions that I wanted to do a project tracking the performance of companies investing in AI data centers. Initially I was going to look at AWS, Google Cloud, and Oracle. My plan was look at their respective growths over the past year, and the month-to-month stability of the stock price. Before moving on to operationalizing what growth or stability looked liked, I started to question the construct validity of these companies. That is, AWS and Google Cloud are divisions of companies that are not connected to data centers. Their prices are going to be influenced by the performance of the larger companies and other extraneous factors. As a result, I decided to pivot and look at companies that work primarily in datacenter real estate. From here, I landed on Equinix (EQIX), Digital Realty (DLR), and Iron Mountain (IRM). However, Iron Mountain is a bit of an outlier as they started in physical document storage and started translating into datacenters. As the medium is still primarily storage in a similar capacity, I figured this would offer interesting comparisons to be made between the three companies

##Advantages of Comparing EQIX, DLR, and IRM

-- These companies are in the same sector
-- These companies have the same asset class
-- These companies are going to receive the same sort of regulatory treatment
-- These companies compete for the similar customers
-- These companies are influenced by similar external factors (e.g., energy costs, interests rates, land pricing)
-- In sum, there is enough congruency between these companies such that the results ascertained from these analyses
-- may help generate real world insight. 

*Operationalization of Stability and Growth*

**Stability**

***Descriptive ***

In order to descriptively look at the stability of growth for each company, I am going to look at the fluctuation of daily stock prices using the range of the price (High - Low) aggregated to the month level. I am then going to compute the coefficient of variation for each month by computing the mean and standard deviation for the range, and dividing the standard deviation by the mean.

Rationale: Initially I wanted to look at daily volatility by working with real time data. However, I do not have the means to collect this type of data. As a result, I opted for the method described above. I did this for a couple of reasons:

The coefficient of variation (CV) is a metric that allows you to compare variability across different metrics. Comparing standard deviations by themselves is difficult and often invalid as metrics can have the same number but different meanings. For instance, a company worth on average $100 with a SD of $15 is much different than a company worth on average $1000 with an SD of $15. The former has 68% of the data falling within $75 and $115, while the latter is $985 to $1015. However, if we computed the CV, the former would be 15% while the latter is 1.5%.

***Inferential ***

In order to assess for statistically significant differences between the stability of growth for each company, I am going to compute a Kruskal-Wallis test with company as the independent variable (three levels: EQIX, DLR, IRM) and CV as the dependent variable. Assuming there is a significant result, I will run a Dunn's test for pairwise comparisons to assess which stability profiles are different from each other.

Rationale: While looking at CVs will allow us to compare the relative variability between companies, it does not tell us whether they are statistically different from each other. A Kruskal-Wallis test followed by a Dunn's test allows us to do this.

*The Kruskal-Wallis*
This is a non-parametric version of an ANOVA. A non-parametric version is necessary as stock data is naturally not normally distributed. Given that we are assuming some growth, these data are naturally going to be positively skewed.

*Dunn's Test*
The Dunn's test is used in order to look at pairwise comparisons between the three companies to assess their statistical differences. This is important as having more than 2 levels increases the chance of type I errors. Dunn's test corrects for this.

**Growth**

***Descriptive***

In order to descriptively look at growth, I will be computing the daily return ((today's close - yesterday's close) / yesterday's close) for each company and running separate linear regressions with time (trading day) as the independent variable and daily return as the dependent variable. The slope will indicate the rate of growth over time, and R² will indicate how consistently the company grew in that direction.

Rationale: Fitting a regression to each company allows us to characterize each company's growth trajectory individually. The slope tells us how fast the stock grew, and R² tells us how consistent that growth was. A high R² means the stock followed a steady upward trend, while a low R² means growth was erratic even if the overall return was positive. Daily return is used as the outcome variable rather than raw close price because it is scale-free, making it comparable across companies trading at very different price levels.

***Inferential***
The same test used in the stability analysis will be used here. The independent variable remains company (three levels: EQIX, DLR, IRM), and the dependent variable will be daily return.

*Statistical Assumptions*

For this project, I am going to be relying on the Kruskal-Wallis test and linear regression. I will be assessing for the following assumptions across the variable types used (CV of stock price range and daily return).

**Independence of Oberservations (Kruskall and Linear Regression)**
This assumption only partially holds. While observations across companies are independent from one another, daily stock prices within each company are not fully independent — previous prices influence current prices. This is known as autocorrelation and is a well-documented property of time series data. This is a known limitation of this analysis and results should be interpreted with this in mind. Explicitly modeling autocorrelation using ARIMA-based methods is identified as a direction for future work.

**Normality of Residuals (Linear Regression)**
Linear regression assumes that the residuals are approximately normally distributed, not the raw data itself. Following each regression, residual plots will be inspected to assess whether this assumption holds. Any meaningful violations will be noted as a limitation.

**Data Source and Time Window**
All data will be sourced from yfinance over a trailing 12-month window. Adjusted close prices will be used rather than raw close prices to account for stock splits and dividends, which would otherwise introduce artificial distortions in the price series.

**Aggregation Period**
The default aggregation period for stability metrics is monthly, consistent with the research question. The pipeline is parameterized to support weekly aggregation without changes to the underlying code.