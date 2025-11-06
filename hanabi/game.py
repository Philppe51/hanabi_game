# Définition des règles du jeu

from typing import List
from .deck import Deck
from .player import Player
from .card import Card, Color

class HanabiGame:
    def __init__(self, player_names: List[str]):
        self.players = [Player(name) for name in player_names]
        self.deck = Deck()
        self.discard_pile: List[Card] = []
        self.played_cards: dict[Color, int] = {
            Color.RED: 0,
            Color.YELLOW: 0,
            Color.GREEN: 0,
            Color.BLUE: 0,
            Color.WHITE: 0,
        }
        self.clues = 8
        self.lives = 3
        self._deal_initial_cards()

    def _deal_initial_cards(self):
        for _ in range(4):  # Chaque joueur reçoit 5 cartes au début
            for player in self.players:
                player.add_card(self.deck.draw())

    def play_card(self, player_index: int, card_index: int) -> bool:
        player = self.players[player_index]
        card = player.play_card(card_index)
        color, value = card.color, card.value

        # Vérifie si la carte peut être jouée
        if self.played_cards[color] + 1 == value:
            self.played_cards[color] = value
            return True
        else:
            self.discard_pile.append(card)
            self.lives -= 1
            return False

    def discard_card(self, player_index: int, card_index: int):
        player = self.players[player_index]
        card = player.discard_card(card_index)
        self.discard_pile.append(card)
        self.clues += 1

    def give_clue(self, giver_index: int, receiver_index: int, clue_type: str, clue_value: str) -> bool:
        if self.clues <= 0:
            return False
        self.clues -= 1
        # Logique pour donner un indice (à implémenter selon vos besoins)
        return True
    
        # Todo
        
