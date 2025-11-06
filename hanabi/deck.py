# Création du deck de cartes 
# 5 couleurs : blanc, bleu, rouge, vert jaune
# 3 cartes de 1
# 2 cartes de 2,3,4
# 1 carte de 5

import random
from typing import List
from .card import Card, Color

class Deck:
    def __init__(self):
        self.cards = self._initialize_deck()
        random.shuffle(self.cards)

    def _initialize_deck(self) -> List[Card]:
        deck = []
        colors = list(Color)
        for color in colors:
            # 3 cartes de valeur 1, 2 cartes de valeur 2-4, 1 carte de valeur 5
            deck.extend([Card(color, 1) for _ in range(3)])
            deck.extend([Card(color, v) for v in range(2, 5) for _ in range(2)])
            deck.append(Card(color, 5))
        return deck

    def draw(self) -> Card:
        return self.cards.pop()
