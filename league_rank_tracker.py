import requests
import json
import mysql.connector
import config

API_KEY = config.API_KEY
CURRENT_SEASON = 'Season 2022'
NAME = 'Bruno'
BRUNO_PUUID = config.BRUNO_PUUID

mydb = mysql.connector.connect(
  host = config.host,
  user = config.user,
  passwd = config.password,
  database = config.database
)

x = requests.get('https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/' + BRUNO_PUUID + '?api_key=' + API_KEY)
y = json.loads(x.text)

riotID = y['id']

x = requests.get('https://na1.api.riotgames.com/lol/league/v4/entries/by-summoner/' + riotID + '?api_key=' + API_KEY)
y = json.loads(x.text)

for i in range(len(y)):
  if (y[i]['queueType'] == 'RANKED_SOLO_5x5'):
    print(y[i]['queueType'])
    tier = (y[i]['tier'])
    rank = (y[i]['rank'])
    leaguePoints = (y[i]['leaguePoints'])
    wins = (y[i]['wins'])
    losses = (y[i]['losses'])
    val = (NAME, CURRENT_SEASON, tier, rank, leaguePoints, wins, losses)

pdo = mydb.cursor()
pdo.execute("SELECT name, season, tier, rank, leaguePoints, wins, losses FROM league_rank_tracker ORDER BY id DESC LIMIT 1")
myresult = pdo.fetchall()

print("Last database entry: " + str(myresult[0]))
print("Current API pull: " + str(val))

if (myresult[0] != val):
  sql = "INSERT INTO league_rank_tracker (name, season, tier, rank, leaguePoints, wins, losses) VALUES (%s, %s, %s, %s, %s, %s, %s)"
  pdo.execute(sql, val)
  mydb.commit()
  
  print(pdo.rowcount, "record(s) inserted.")
else:
  print('No change.')