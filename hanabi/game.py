# Définition des règles du jeu

from typing import List, Optional, Tuple
from enum import Enum
from typing import List
from .deck import Deck
from .player import Player
from .card import Card, Color

class ClueType(Enum):
    COLOR = "color"
    VALUE = "value"

class Clue:
    def __init__(self, clue_type: ClueType, value: Optional[str], color: Optional[Color]):
        self.type = clue_type
        self.value = value  # Ex: "1", "2", ..., "5"
        self.color = color  # Ex: Color.RED
        self.target_player_index = None  # À définir lors de l'envoi
        

    def apply_to_player(self, player: Player) -> List[int]:
        """Retourne les indices des cartes dans la main du joueur qui correspondent à l'indice."""
        indices = []
        for i, card in enumerate(player.hand):
            if (self.type == ClueType.COLOR and card.color == self.color) or \
               (self.type == ClueType.VALUE and str(card.value) == self.value):
                indices.append(i)
        return indices



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
        self.clues_history = []  # Stocke les indices donnés
        self.clues_available = 8  # Nombre d'indices restants
        self.turn_count = 0
    
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

    def give_clue(self, giver_index: int, receiver_index: int, clue_type: ClueType, value: str = None, color: Color = None) -> bool:
        if self.clues_available <= 0:
            return False

        receiver = self.players[receiver_index]
        clue = Clue(clue_type, value, color)
        affected_indices = clue.apply_to_player(receiver)

        # Stocke l'indice dans l'historique
        self.clues_history.append(ClueRecord(
            giver_index=giver_index,
            receiver_index=receiver_index,
            clue_type=clue_type,
            value=value,
            color=color,
            affected_indices=affected_indices,
            turn=self.turn_count
        ))

        # Stocke l'indice sur le joueur receveur
        if not hasattr(receiver, 'clues'):
            receiver.clues = [[] for _ in range(len(receiver.hand))]
        for idx in affected_indices:
            if clue_type == ClueType.COLOR:
                receiver.clues[idx].append(("couleur", color.name))
            else:
                receiver.clues[idx].append(("valeur", value))

        self.clues_available -= 1
        return True

    def discard_card(self, player_index: int, card_index: int):
        player = self.players[player_index]
        card = player.discard_card(card_index)
        self.discard_pile.append(card)
        self.clues_available = min(self.clues_available + 1, 8)  # Max 8 indices


