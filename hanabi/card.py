# Définition des différentes cartes

from enum import Enum, auto

class Color(Enum):
    RED = auto()
    YELLOW = auto()
    GREEN = auto()
    BLUE = auto()
    WHITE = auto()

class Card:
    def __init__(self, color: Color, value: int):
        self.color = color
        self.value = value  # 1 à 5
        self.clues = [] # Liste des indices associés à cette carte

    def add_clue(self, clue_type: str, clue_value: str):
        self.clues.append((clue_type, clue_value))

    def clear_clues(self):
        self.clues = []

    def __repr__(self):
        return f"Card(color={self.color.name}, value={self.value})"
