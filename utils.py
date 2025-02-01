from bs4 import BeautifulSoup

def parse_player_info(player_info_soup: BeautifulSoup) -> dict:
    '''Parse player information from player page'''

    # Extract player information
    player_info = {}

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


def table_parse(table_html: BeautifulSoup) -> list:
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
