import pandas as pd
from os import path
import nhl_abbreviations
pd.options.mode.copy_on_write = True

'''
This  program will construct a DataFrame of desired statistics of NHL players 
that have previously participated in the U20 IIHF World Junior championship.
'''

DATA_DIR = "/Users/raphaelswitzer/Documents/raphaels_work/Personal"


# Creating Dataframe of World Juniors data
wjc = pd.read_csv(path.join(DATA_DIR, "2013_World_Juniors.csv"))


wjc_list = [wjc]
for i in range(14, 20):
    new_wjc = pd.read_csv(path.join(DATA_DIR, str(2000 + i) + '_World_Juniors.csv')).reset_index(drop=True)
    wjc_list.append(new_wjc)

wjc = pd.concat(wjc_list, ignore_index=True)
wjc = wjc[['Name', 'GP', 'GWG', 'P']]

# Creating a DataFrame of each player's total world junior stats
for i in wjc.columns[1:]:
    wjc[i] = wjc[i].astype(float)
wjc["Name"] = wjc["Name"].astype(str)
wjc_total = wjc.groupby('Name').agg({'GP': 'sum', 'GWG': 'sum', 'P': 'sum'})
wjc_total["P/GP"] = wjc_total["P"] / wjc_total['GP']
wjc_total.to_csv(path.join(DATA_DIR, 'wjc_total.csv'))

# Creating a DataFrame of Playoff Data
po_stats = pd.read_csv(path.join(DATA_DIR, "2015_NHL_Playoffs.csv"))
po_stats.columns = po_stats.iloc[0]
po_stats = po_stats.iloc[1:].reset_index(drop=True)
po_stats["Year"] = 2015
po_list = [po_stats]
for i in range(16,24):
    new_po = pd.read_csv(path.join(DATA_DIR, '20' + str(i) + '_NHL_Playoffs.csv'))
    new_po.columns = new_po.iloc[0]
    new_po = new_po.iloc[1:].reset_index(drop=True)
    new_po["Year"] = 2000 + i
    po_list.append(new_po)

po_stats = pd.concat(po_list, ignore_index=True)
for i in po_stats.columns[5:10]:
    po_stats[i] = po_stats[i].astype(float)

po_stats.to_csv(path.join(DATA_DIR, "po_stats.csv"))

# Extract important columns and merge world junior data with playoff data
wjc_po_stats = pd.merge(wjc_total,po_stats, left_on='Name', right_on='Player')
wjc_po_stats.columns = ['WJC_GP', 'WJC_GWG', 'WJC_P', 'WJC_P/GP', 'Rk', 'Player', 'Age', 'Team', 'Pos', 'PO_GP',
       'G', 'A', 'PTS', '+/-', 'PIM', 'EV', 'PP', 'SH', 'GW', 'EV', 'PP', 'SH',
       'S', 'S%', 'TOI', 'ATOI', 'BLK', 'HIT', 'FOW', 'FOL', 'FO%', 'Year']
wjc_po_stats = wjc_po_stats[['WJC_GP', 'WJC_GWG', 'WJC_P', 'WJC_P/GP', 'Player', 'Team', 'PO_GP',
       'G', 'A', 'PTS', 'Year']]
wjc_po_stats.to_csv("/Users/raphaelswitzer/Documents/raphaels_work/Personal/wjc_po_stats.csv")

# Creating a DataFrame of Regular Season Data
season_stats = pd.read_csv(path.join(DATA_DIR, "2015_NHL_STATS.csv"))

season_stats["Year"] = 2015
season_list = [season_stats]
for i in range(16,24):
    new_season = pd.read_csv(path.join(DATA_DIR, '20' + str(i) + '_NHL_STATS.csv'))
    new_season["Year"] = 2000 + i
    season_list.append(new_season)

season_stats = pd.concat(season_list, ignore_index=True)
season_stats = season_stats[['Player', 'Age', 'Team', 'Pos', 'GP', 'G', 'A', 'PTS', 'Year']]
season_stats.columns = ['Player', 'Age', 'Team', 'Pos', 'Season_GP', 'Season_G', 'Season_A', 'Season_PTS', 'Year']
season_stats.to_csv(path.join(DATA_DIR, "season_stats.csv"))

# merge season data with playoff and world junior data

szn_wjc_po = pd.merge(wjc_po_stats, season_stats, on=['Player', 'Year'])
szn_wjc_po["Season_PTS/GP"] = szn_wjc_po["Season_PTS"] / szn_wjc_po["Season_GP"]
szn_wjc_po = szn_wjc_po.drop("Team_y", axis=1)
szn_wjc_po = szn_wjc_po.rename(columns={"Team_x" : "Team"})
szn_wjc_po.to_csv(path.join(DATA_DIR, 'szn_wjc_po.csv'))

# Creating Dataframe of NHL Standings data

standings = pd.read_csv(path.join(DATA_DIR, "2015_NHL_Standings.csv"))
standings = standings.dropna()

standings = standings.rename(columns={'Unnamed: 1': 'Team'})

standings = standings[['Rk', 'Team', 'AvAge', 'GP', 'W', 'L', 'OL', 'PTS', 'PTS%']]
standings["Year"] = 2015

standings_list = [standings]

for i in range(16,24):
    new_standings = pd.read_csv(path.join(DATA_DIR, '20' + str(i) + '_NHL_Standings.csv'))
    new_standings = new_standings.dropna()
    new_standings.rename(columns={"Unnamed: 1": 'Team'}, inplace=True)
    new_standings = new_standings[['Rk', 'Team', 'AvAge', 'GP', 'W', 'L', 'OL', 'PTS', 'PTS%']]
    new_standings["Year"] = 2000 + i
    standings_list.append(new_standings)

standings = pd.concat(standings_list, ignore_index=True)

standings.to_csv(path.join(DATA_DIR, 'standings.csv'))

points = standings[["Team", "Year", "PTS%"]]
points.rename({"PTS%": "Team_PTS%"}, inplace=True)
points["Team"] = points["Team"].str.replace("*", "")
points["PTS%"] = points["PTS%"].astype(float)
points.to_csv(path.join(DATA_DIR,"points.csv"))


# get dictionary of team abbreviations to convert team names to abbreviations for the merge
abb_dict = nhl_abbreviations.get_abbreviations()

points["Team"] = points["Team"].map(abb_dict)

desired_stats = pd.merge(szn_wjc_po, points, on=["Team", "Year"])

desired_stats.rename(columns={"G": "PO_G", "A": "PO_A", "PTS": "PO_PTS", "PTS%": "Team_PTS%"},inplace=True)

desired_stats["PO_PTS/GP"] = desired_stats["PO_PTS"]/desired_stats["PO_GP"]
final_desired_stats = desired_stats[['Player', 'Pos', 'Team', 'WJC_GP', 'WJC_GWG', 'WJC_P', 'WJC_P/GP', 'Year',
        'Season_GP', 'Season_PTS/GP', 'Team_PTS%', 'PO_GP', 'PO_PTS', 'PO_PTS/GP']]
final_desired_stats.to_csv(path.join(DATA_DIR,"final_desired_stats.csv"))



