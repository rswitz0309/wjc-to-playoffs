# WJC and NHL Playoffs Analysis – Full Report

## 1. Introduction

This report investigates the potential relationship between a player’s performance in the IIHF U20 World Junior Championship (WJC) and their later performance in the NHL playoffs. The goal is to evaluate whether WJC performance can serve as a meaningful predictive factor for future playoff outcomes using statistical and machine learning models.

---

## 2. Data Collection

### Sources:
- **WJC Player Stats:** QuantHockey.com  
- **NHL Regular Season and Playoff Stats:** Hockey-Reference.com

### Data Scope:
- Players who participated in the WJC and later played in the NHL playoffs
- Seasons included: 2013-2019 (World Juniors, 2015-2023 (Regular Season and Playoffs)
- Variables collected: goals, assists, points, games played, team points % (PTS%), 

---

## 3. Data Preprocessing

- Merged datasets by player-season
- Accessed the NHL API to create a dictionary of team name and abbreviations using requests library
- Created derived features:
  - WJC PPG
  - NHL Regular Season PPG
  - Playoff PPG
  - NHL regular season and playoff year


---

## 4. Exploratory Data Analysis 

- Correlation heatmaps to assess linear relationships
- Visualizations:
  - [Relationship between WJC PPG and NHL playoff PPG](https://github.com/rswitz0309/wjc-to-playoffs/blob/main/visuals%3A/wjc_po.png)
  - [Relationship between regular season PPG and playoff PPG](https://github.com/rswitz0309/wjc-to-playoffs/blob/main/visuals%3A/season_po.png)

**Key Observations:**
- Players with high regular season PPG tended to maintain higher playoff performance.
- WJC PPG showed weak correlation with playoff points.
  

---

## 5. Statistical Modeling

### 5.1 OLS Linear Regression (Statsmodels)

- **Target Variable:** NHL Playoff Points Per Game
- **Independent Variables:** WJC PPG, Regular Season PPG, WJC GP, Team PTS%, Playoff GP

**Model Summary:**
[OLS regression summary](https://github.com/rswitz0309/wjc-to-playoffs/blob/main/visuals%3A/ols_regression_summary.pdf)
- R²: 0.487
- Significant variables (p < 0.05): Regular Season PPG, Playoff GP
- Regular Season PPG Coefficient: 0.8068, p-value: 0.0000
- Playoff GP Coefficient: 0.0139, p-value: 0.0000
- WJC PPG Coefficient: 0.0125, p-value: 0.6685

**Interpretation:**
- WJC performance was not statistically significant meaning it should not be considered as a factor for predicting playoff performance on its own.
- Regular Season performance was statistically significant and had a relatively strong direct relationship with playoff performance.
- Playoff GP was statistically significant and indicated that typically players perform better if their team goes far in the playoffs.

---

### 5.2 Random Forest Regression (Scikit-learn)

- Trained on same variables as the OLS model as well as player position, WJC points, WJC game-winning goals

**Model Metrics:**
- MAE: ~0.25 PPG

**Top Predictors (by feature importance):**
Season_PTS/GP    0.602425
PO_GP            0.123461
Team_PTS%        0.081419
WJC_P/GP         0.063057
WJC_P            0.043023
WJC_GP           0.037208
WJC_GWG          0.017991
C                0.010731
LW               0.007959
D                0.007466
RW               0.004840
F                0.000420
**Interpretation:**
- Considering this is a playoff prediction model, a MAE of 0.25 PPG shows that this model is quite strong at predicting playoff performance given that the maximum amount of games in a playoff season that a player would play is around 25 games
- Season points per game contributed by far the most to the model
- World Junior points per game added some value to the predictions

---

## 6. Conclusion

- WJC performance alone is a weak predictor of NHL playoff success.
- Regular season performance and draft position are stronger and more reliable predictors.
- WJC stats may still offer some value when used alongside other indicators.

---

## 7. Limitations

- Sample size may be biased toward players who made it to the NHL playoffs
- Only the top 150 players from each WJC year were included 
- Performance context (e.g., linemates) were not accounted for


---

## 8. References

- [QuantHockey.com](https://www.quanthockey.com/)
- [Hockey-Reference.com](https://www.hockey-reference.com/)
- [Statsmodels Documentation](https://www.statsmodels.org/)
- [Scikit-learn Documentation](https://scikit-learn.org/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Requests Documentation](https://requests.readthedocs.io/en/latest/)


