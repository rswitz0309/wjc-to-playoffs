# World Juniors and NHL Playoffs Analysis
A machine learning and analytics project examining the relationship between U20 IIHF World Junior Championship performance and NHL playoff outcomes.
## Datasets
World Junior player performance data were obtained from QuantHockey.com  
Team and player regular season performance and playoff player performance data were obtained from Hockey-Reference.com
## Methodology
The analysis was conducted using Python and various libraries for data manipulation, visualization, and modeling:
### Data Cleaning & Processing:
pandas for loading, cleaning, and transforming datasets
Data merging based on player names and seasons
### Visualization & Exploratory Analysis:
seaborn and matplotlib for correlation heatmaps
### Statistical Modeling:
statsmodels for OLS regression, including summary statistics and p-values for feature interpretability
scikit-learn for Random Forest Regression to evaluate feature importance and nonlinear relationships
## Key Questions
Can standout World Junior performances forecast a player’s impact in the NHL playoffs?
Which features (e.g., world junior PPG, regular season GP, regular season PPG) contribute most to playoff performance?
How strong is the correlation between WJC and NHL playoff performance metrics?
## Results 
The OLS Regression model showed limited predictive power using WJC stats alone but high predictive power using Regular Season PPG.
The Random Forest model suggested that regular season performance metrics were far more influential.
World Junior performance, while not a strong standalone predictor, may still serve as a complementary variable in broader predictive models.
## Conclusion
It was determined that World Junior player performance should not be considered a strong indicator of determining future NHL playoff performance on its own, however, it may help to generate predictions along with other significant variables such as regular season PPG.
