*Context*

I wanted to do a project that utilized live data, and came to the conclusions that I wanted to do a project tracking the performance of companies investing in AI data centers. Initially I was going to look at AWS, Google Cloud, and Oracle. My plan was look at their respective growths over the past year, and the month-to-month stability of the stock price. Before moving on to operationalizing what growth or stability looked liked, I started to question the construct validity of these companies. That is, AWS and Google Cloud are divisions of companies that are not connected to data centers. Their prices are going to be influenced by the performance of the larger companies and other extraneous factors. As a result, I decided to pivot and look at companies that work primarily in datacenter real estate. From here, I landed on Equinix (EQIX), Digital Realty (DLR), and Iron Mountain (IRM). However, Iron Mountain is a bit of an outlier as they started in physical document storage and started translating into datacenters. As the medium is still primarily storage in a similar capacity, I figured this would offer interesting comparisons to be made between the three companies

**Advantages of Comparing EQIX, DLR, and IRM**

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

In order to descriptively look at the stability of growth for each company, I am going to look at the flucuation of daily stock prices use the range of the price (High - Low) aggregated to the month level. I am then going to compute the coefficient of variation for each month by computing the mean and standard deviation for the range, and dividing the standard deviation by the mean

Rationale: Intiailly I wanted to look at daily volatility by working with real time data. However, I do not have the means to collect this type of data. As a result, I opted for the method described above.  I did this for a couple of reasons:

-1 coefficient of variation (CV) is a metric that allows you to compare variability across different metrics. Comparing standard deviations by themselves is difficult and often invalid as metrics can have the same number but different meanings. For instance, a company worth on average $100 with a SD of $15 is much different than a company worth on average $1000 with an SD of $15. The former has 68% of the data falling within $75 and $115, while the the latter is $9975 to $1015. However, if we computed the CV, the former would be 15% while the latter is 1.5%

***Inferential ***

In order to assess for statistically significant differences between the stability of growth for each company, I am going to compute a Kruskal-Wallis test with three levels. Assuming there is a significant results, I will run a Dunn's test for pairwise comparisons to assess which stability averages are difference form each other. In both cases, I will be using the CV (as mentioned above).

Rationale: While looking at CVs will allow us to compare the relative variability between, it does not tell us is the are statistically different from each other. A Kruskall-Wallis test follow by a Dunn's test allows us to do this. The Kruskall-Wallis is a non-parametric version of an ANOVA. this is necessary as stock data is naturally not normally distributed. In other words, given we are assuming some growth, that suggest that these data are naturally going to be positively skewed. The Dunn's test is use in order to look at pairwise comparisons between the three companies to assess their statistical difference. This is important as having more than 2 IVs increases the chance of type I errors. Dunn's test allows us to correct for this. 

**Growth**

***Descriptive ***

In order to look at growth, I will be computing the daily return ((today's close - yesterday's close) / yesterday's close) and running separate linear regressions for each company to assess their growth trends. the slope will allow us to see how fast the stock grew, and R^2 will show how consistent it grew in the slopes direction

rationale: fitting a regression to each company will allow us to descriptively look at each companies growth. specifically, we will be able to see the rate in strength and direction the a companies return change for each increase in time (e.g., months, year). 


***Inferential ***

The same computations that were used in stability analyses will be used here. The only difference is the metric will be based on the daily return

Rationale: While looking at the growth trends as measure by changes in daily return over time, it does not tell us is the are statistically different from each other. A Kruskall-Wallis test follow by a Dunn's test allows us to do this. The Kruskall-Wallis is a non-parametric version of an ANOVA. this is necessary as stock data is naturally not noramlly distributed. In other words, given we are assuming some growth, that suggest that these data are naturally going to be positively skewed. The Dunn's test is use in order to look at pariwise comparisons between the three companies to assess their statistical difference. This is important as having more than 2 IVs increases the chance of type I errors. Dunn's test allows us to correct for this. 