# Définition des joueurs et de leurs interactions

from typing import List
from .card import Card

class Player:
    def __init__(self, name: str):
        self.name = name
        self.hand = []


    def add_card(self, card: Card):
        self.hand.append(card)

    def play_card(self, index: int) -> Card:
        return self.hand.pop(index)

    def discard_card(self, index: int) -> Card:
        return self.hand.pop(index)

    def __repr__(self):
        return f"Player(name={self.name}, hand_size={len(self.hand)})"

