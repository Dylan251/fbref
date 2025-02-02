from dataclasses import dataclass

@dataclass
class Club:
    '''Class for club data'''
    name: str
    url: str
    players: list