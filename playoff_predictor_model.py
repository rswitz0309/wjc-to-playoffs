import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import pandas as pd
from os import path

from pandas import Series
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import statsmodels.formula.api as smf
import seaborn as sns

'''
This program uses a DataFrame containing World Junior, Regular Season and Playoff performance
from players who have played in the NHL to build models and develop insights about the data. 
It will help to determine relationships between variables and build a model 
to generate predictions about an NHL player's playoff performance.
'''

DATA_DIR = "/Users/raphaelswitzer/Documents/raphaels_work/Personal"

final_desired_stats = pd.read_csv(path.join(DATA_DIR,"final_desired_stats.csv"))

# Getting statistics out of a linear regression model to develop insights

wjc_model = smf.ols(formula="Q('PO_PTS/GP') ~ WJC_GP + WJC_GWG + Q('WJC_P/GP') + Q('Season_PTS/GP') + Q('Team_PTS%') + PO_GP", data=final_desired_stats)
results = wjc_model.fit()
print(results.summary2())

# Build models to predict playoff performance

cont_vars_wjc = ['WJC_GP', 'WJC_GWG', 'WJC_P', 'WJC_P/GP','Season_GP', 'Season_PTS/GP',
             'Team_PTS%', 'PO_GP']

cont_vars= ['Season_GP', 'Season_PTS/GP', 'Team_PTS%', 'PO_GP']

df_pos = pd.concat([pd.get_dummies(final_desired_stats['Pos'])], axis=1)

po_predict_wjc_df = pd.concat([df_pos, final_desired_stats[cont_vars_wjc]], axis=1)
playoff_predictor_df = pd.concat([df_pos, final_desired_stats[cont_vars]], axis=1)

po_predict_wjc_df['PO_PTS/GP'] = final_desired_stats['PO_PTS/GP']
playoff_predictor_df['PO_PTS/GP'] = final_desired_stats['PO_PTS/GP']

xvars_wjc = cont_vars_wjc + list(df_pos.columns)
xvars = cont_vars + list(df_pos.columns)
yvar = 'PO_PTS/GP'

# Test both models

train1, test1 = train_test_split(po_predict_wjc_df, test_size=0.20)
train2, test2 = train_test_split(playoff_predictor_df, test_size=0.20)

model_wjc = RandomForestRegressor(n_estimators=10000)
model = RandomForestRegressor(n_estimators=10000)

model_wjc.fit(train1[xvars_wjc], train1[yvar])
model.fit(train2[xvars], train2[yvar])

test1['PO_PTS/GP_wjc_hat'] = model_wjc.predict(test1[xvars_wjc])
test2['PO_PTS/GP_hat'] = model.predict(test2[xvars])

# Evaluating model performance

print(mean_absolute_error(test1[yvar], test1['PO_PTS/GP_wjc_hat']))
print(mean_absolute_error(test2[yvar], test2['PO_PTS/GP_hat']))

# Checking  relationship of variables and
# determining which variables contributed the most to the model
print(Series(model_wjc.feature_importances_, xvars_wjc).sort_values(ascending=False))
print(Series(model.feature_importances_, xvars).sort_values(ascending=False))

print(final_desired_stats[cont_vars_wjc].corr())

# Visualizations

g = sns.FacetGrid(final_desired_stats).map(sns.kdeplot, 'WJC_P/GP', 'PO_PTS/GP')
g.fig.subplots_adjust(top=0.9)
g.fig.suptitle("Playoff Performance vs. World Junior Performance")
g.savefig(path.join(DATA_DIR, 'wjc_po.png'))
g = sns.FacetGrid(final_desired_stats).map(sns.kdeplot, 'Season_PTS/GP', 'PO_PTS/GP')
g.fig.subplots_adjust(top=0.9)
g.fig.suptitle("Playoff Performance vs. Regular Season Performance")
g.savefig(path.join(DATA_DIR, 'season_po.png'))
