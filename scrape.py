from bs4 import BeautifulSoup
import requests as r



def parse_player_info(player_info_soup):
    '''Parse player information from player page'''

    # Extract player information
    player_info = {}
    print(player_info_soup)

    # Position and Footed
    p_player_info = player_info_soup.findAll('p')

    if p_player_info[0]:
        try:
            position_p, position_footed = p_player_info[0].text.split('▪')

            # Parse position and footed
            player_info['Position'] = position_p.split(':')[1].strip()
            player_info['Footed'] = position_footed.split(':')[1].strip()
        except:
            pass

        position_p = p_player_info[0].text.split(':')[1].strip()
        player_info['Position'] = position_p

    # Age
    if p_player_info[1]:
        player_info['age'] = p_player_info[1].text.split(':')[1].strip()

    # Wikipedia Link
    if p_player_info[-1]:
        player_info['wikipedia'] = p_player_info[-1].find('a')['href']

    return player_info


def table_parse(table_html):
    '''Table parser function'''
    # Extract headers
    headers = [th.get_text(strip=True) for th in table_html.find('thead').find_all('th')]

    # Extract rows
    rows = []
    for row in table_html.find('tbody').find_all('tr'):
        cells = row.find_all(['th', 'td'])
        row_data = {}
        for header, cell in zip(headers, cells):
            row_data[header] = cell.get_text(strip=True)
        rows.append(row_data)
    
    return rows


url = 'https://fbref.com/en/squads/822bd0ba/2024-2025/roster/Liverpool-Roster-Details'

# Fetch HTML
html_content = r.get(url).text


# Make soup
soup = BeautifulSoup(html_content, 'html.parser')

# Initialize a list to store all players' data
all_players = []

# Find all player blocks
player_blocks = soup.find_all(['h2', 'div'], recursive=True)

print(len(player_blocks))

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
