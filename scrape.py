from bs4 import BeautifulSoup
import requests as r

from utils import parse_club_players


# Fetch club urls


# Fetch 






url = 'https://fbref.com/en/squads/822bd0ba/2024-2025/roster/Liverpool-Roster-Details'

# Fetch HTML
html_content = r.get(url).text

# Make soup
soup = BeautifulSoup(html_content, 'html.parser')

all_players = parse_club_players(soup)

# Print the extracted data
for player in all_players:
    print("Player Name:", player.get('Name'))
    print("Player Info:", player.get('Info'))
    print("Table Data:")
    for row in player.get('Table', []):
        print(row)
    print("\n---\n")

