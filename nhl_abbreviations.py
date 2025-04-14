import requests

'''
Here is a function that scrapes data from the NHL API to be able to access
information about NHL team abbreviations
'''
def get_abbreviations():
    '''
    This function accesses the NHL API to create a dictionary for Team abbreviations
    :return: A dictionary containing team abbreviations
    '''
    url = "https://api-web.nhle.com/v1/standings/2025-04-08"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        teams = data['standings']

        # Dictionary of abbreviations and team names
        nhl_teams = {}

        for team in teams:
            abbreviation = team['teamAbbrev']['default']
            name = team['teamName']['default']
            nhl_teams[name] = abbreviation
        return nhl_teams
