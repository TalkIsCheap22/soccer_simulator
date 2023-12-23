from bs4 import BeautifulSoup
import urllib.request
import csv
import json

url_team_ha = "https://1x2stats.com/en-gb/ENG/2022/Premier-League/"
player_file = "../players.csv"
#url_player = "https://fbref.com/en/comps/9/2022-2023/stats/2022-2023-Premier-League-Stats"

def read_team_ha():
    teams = []
    html = urllib.request.urlopen(url_team_ha).read().decode('utf-8')   
    soup = BeautifulSoup(html, 'lxml')
    table = soup.body.div.div.next_sibling.div.next_sibling.div.div.next_sibling.next_sibling.div.table
    stats = table.tbody.find_all('tr')
    for stat in stats:
        team = {}
        datas = stat.find_all('td')
        name = datas[0].string
        home_goals = int(datas[12].string)
        home_losses = int(datas[13].string)
        away_goals = int(datas[17].string)
        away_losses = int(datas[18].string)
        team["name"] = name
        team["prev_home_goals"] = home_goals
        team["prev_away_goals"] = away_goals
        team["prev_home_losses"] = home_losses
        team["prev_away_losses"] = away_losses
        team["prev_home_matches"] = 19
        team["prev_away_matches"] = 19
        team["players"] = []
        teams.append(team)
    return teams

def read_player(dict):
    with open(player_file, mode="r", encoding="utf-8-sig") as file:
        reader = csv.reader(file)
        header = next(reader)
        curr_team = None
        for row in reader:
            team_name = row[4]
            if curr_team == None or curr_team["name"] != team_name:
                for item in dict:
                    #print("item[name]={a}, team_name={b}".format(a=curr_team["name"],b=team_name))
                    if item["name"] == team_name:
                        curr_team = item
                        break
            player = {}
            player["name"], player["prev_goals"], player["prev_assists"] = row[1], int(row[10]), int(row[46])
            curr_team["players"].append(player)
    return dict
    

dict = {}
dict["name"] = "Premier League"
dict["tot_rounds"] = 38
dict["teams"] = read_team_ha()
dict["teams"]= read_player(dict["teams"])
for team in dict["teams"]:
    team_goals, player_goals = team["prev_home_goals"] + team["prev_away_goals"], 0
    for player in team["players"]:
        player_goals += player["prev_goals"]
    if player_goals > team_goals:
        team["prev_home_goals"] += ((player_goals - team_goals + 1) / 2)
        team["prev_away_goals"] = player_goals - team["prev_home_goals"]
ans = json.dumps(dict)
print(ans)
