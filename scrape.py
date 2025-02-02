from bs4 import BeautifulSoup
import requests as r
from utils import parse_club_players, parse_club


# Fetch club urls
def fetch_club_details(url):
    '''Fetch club urls from the main page'''
    
    # Fetch HTML
    html_content = r.get(url).text

    # Make soup
    soup = BeautifulSoup(html_content, 'html.parser')
    content = soup.find('div', id='content')
    table = content.find('div', class_='table_wrapper')

    clubs_data = []

    # Iterate through each row in the table body
    for row in table.find('tbody').find_all('tr'):
        # Find the team cell
        team_cell = row.find('td', {'data-stat': 'team'})
        team_dict = parse_club(team_cell)
        if team_dict:
            clubs_data.append(team_dict)
    
    return clubs_data


# Fetch club players
def fetch_club_players(url: str):
    '''Fetch club players from the club page'''

    # Fetch HTML
    html_content = r.get(url).text

    # Make soup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Parse club players
    all_players = parse_club_players(soup)

    return all_players


def main():
    '''Main function'''

    premier_league_url = 'https://fbref.com/en/comps/9/Premier-League-Stats'

    # Fetch club urls
    club_objects = fetch_club_details(premier_league_url)

    # Fetch club players
    for club in club_objects:
        club.players = fetch_club_players(club.url)


