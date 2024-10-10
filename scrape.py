import requests
from bs4 import BeautifulSoup
import json
import random

id = 1
players = []

def scrape(nr: str):
    print(nr)
    global id
    url = "https://www.worldfootball.net/players_list/bundesliga-2024-2025/nach-mannschaft/" + nr + "/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', class_='standard_tabelle')

    global players

    for row in table.find_all('tr')[1:]:  # Skipping the header row
        cols = row.find_all('td')
        if len(cols) > 1:
            player_name = cols[0].text.strip()
            club = cols[2].text.strip()
            position = cols[5].text.strip()
            player_dict = {
                "id": str(id),
                "name": player_name,
                "position": get_position(position),
                "club": club,
                "status": random.randint(1, 6),
                "potential": random.randint(1, 6), 
                "chemistry": 0.5, 
                "price": random.randint(15, 25), 
                "scouting_price": random.randint(5, 14)
            }
            id += 1
            players.append(player_dict)
    print(id)

def get_position(pos: str):
    if pos == "GK":
        return "GOALKEEPER"
    if pos == "DF":
        return "DEFENDER"
    if pos == "MF":
        return "MIDFIELDER"
    if pos == "FW":
        return "STRIKER"
    
for nr in range(1,12):
    scrape(str(+nr))
    
players_json = json.dumps(players, indent=4)
with open('players2.json', 'w') as f:
        f.write(players_json)