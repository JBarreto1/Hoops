#Is it true that Lamarcus Aldridge, Brandon Roy, and Greg Oden played in 62 games together and they went 50-12 in total?

import requests
import json

#Oden only played for the Blazers two season: 08-09 and 09-10
#Aldridge id: 6
#Oden: 1798
#Brandon Roy: 1689
#portland: 25

# query = {'player_ids':'1'}
# response = requests.get("https://www.balldontlie.io/api/v1/stats",
# params=query)
# print(response.url)

# query = {'team_ids[]':'25','seasons[]':['2008','2009']}
# response = requests.get("https://www.balldontlie.io/api/v1/games",params=query)

# response = requests.get("https://www.balldontlie.io/api/v1/players/1798")

# gameIDs = ['22505','22854']
# playerIDs = ['6','1798','1689']
# # playerIDs = ['1798']
# seasonIDs = ['2009','2008']
# query = {'seasons[]':seasonIDs,'player_ids[]':playerIDs}
# response = requests.get("https://www.balldontlie.io/api/v1/stats",params=query)
# print(response.url)

# data = response.json()['data']

def accStats(pID,page):
    #Request the data from the free API
    seasonIDs = ['2009','2008']
    query = {'seasons[]':seasonIDs,'player_ids[]':pID,'per_page':'100','page':page}
    response = requests.get("https://www.balldontlie.io/api/v1/stats",params=query)
    print(response.url)
    return response.json()

def gamesPlayed(playerIDs):
    morePages = True
    data = []
    page = 1
    while morePages:
        #Data comes in through pages at 100 lines per page
        newData = accStats(playerIDs,page)
        data = data + newData['data']
        if newData['meta']['next_page'] is None:
            morePages = False
        else:
            page += 1
    gameIDs = {}
    #Each line of data is a stat line for a player for a game
    for game in data:
        if game['min'] is not None:
            #Sometimes players are injured but still appear on the roster. If they DNP, they're zero, looks like if they didn't suit up, it's NULL
            gID = str(game['game']['id'])
            if gID not in gameIDs.keys():
                #accumulate whether each player played in the game and whether it was a win or loss
                gameDict = {
                    'win': winLoss(game['game']),
                    '6': False,
                    '1689': False,
                    '1798': False
                }
                gameDict[str(game['player']['id'])] = True
                gameIDs[gID] = gameDict
            else:
                gameIDs[gID][str(game['player']['id'])] = True
    wins = 0
    losses = 0
    for outCome in gameIDs.values():
        if outCome['6'] and outCome['1689'] and outCome['1798']:
            #Did all three play? What was the outcome if so?
            print(outCome)
            if outCome['win']:
                wins += 1
            else:
                losses += 1
    return [wins,losses]

def winLoss(data):
    #Given the data line for a particular game indicate with Portland won or loss
    win = False
    if data['home_team_id'] == 25:
        if data['home_team_score'] > data['visitor_team_score']:
            win = True
    if data['visitor_team_id'] == 25:
        if data['home_team_score'] < data['visitor_team_score']:
            win = True
    return win


if __name__ == '__main__':
    playerIDs = ['6','1798','1689']
    #Used the API's search to find the IDs of the three players I'm interested in
    print(gamesPlayed(playerIDs))