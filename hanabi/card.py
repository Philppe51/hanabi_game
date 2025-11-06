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

    def __repr__(self):
        return f"Card(color={self.color.name}, value={self.value})"
