from bs4 import BeautifulSoup
import requests as r

from .utils import parse_player_info, table_parse


url = 'https://fbref.com/en/squads/822bd0ba/2024-2025/roster/Liverpool-Roster-Details'

# Fetch HTML
html_content = r.get(url).text


# Make soup
soup = BeautifulSoup(html_content, 'html.parser')

# Initialize a list to store all players' data
all_players = []

# Find all player blocks
player_blocks = soup.find_all(['h2', 'div'], recursive=True)

# Temporary variables to store player info and table data
current_player = {}
current_table = None

# Iterate through the player blocks
for block in player_blocks:
    # Check if the block is a player name (h2 tag)
    if block.name == 'h2':
        # If we have a current player, add them to the list
        if current_player:
            all_players.append(current_player)
            current_player = {}  # Reset for the next player

        # Extract player name
        player_name = block.get_text(strip=True)
        current_player['Name'] = player_name

    # Check if the block is player info (div with display:flex)
    elif block.name == 'div' and 'style' in block.attrs and 'display:flex' in block['style']:
        # Extract player info
        player_info = {}
        info_div = block.find('div', class_='roster-player-info')

        player_info = parse_player_info(info_div)

        # Add player info to the current player
        current_player['Info'] = player_info

    # Check if the block is a table wrapper (div with class table_wrapper)
    elif block.name == 'div' and 'class' in block.attrs and 'table_wrapper' in block['class']:
        # Extract table data
        table_data = table_parse(block)

        # Add table data to the current player
        current_player['Table'] = table_data

# Add the last player to the list
if current_player:
    all_players.append(current_player)

# Print the extracted data
for player in all_players:
    print("Player Name:", player.get('Name'))
    print("Player Info:", player.get('Info'))
    print("Table Data:")
    for row in player.get('Table', []):
        print(row)
    print("\n---\n")

# # Get Tables
# html_tables = soup.find_all('div', class_='table_wrapper')

# rows = table_parse(html_tables[1])

# print(len(html_tables))
# print(rows)
