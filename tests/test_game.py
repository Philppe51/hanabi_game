
import pytest
from hanabi.game import HanabiGame
from hanabi.card import Color

def test_initial_deal():
    game = HanabiGame(["Alice", "Bob"])
    assert len(game.players) == 2
    assert len(game.players[0].hand) == 4
    assert len(game.players[1].hand) == 4

def test_play_card():
    game = HanabiGame(["Alice"])
    # Simuler une carte jouable
    game.players[0].hand[0].color = Color.RED
    game.players[0].hand[0].value = 1
    assert game.play_card(0, 0) is True
    assert game.played_cards[Color.RED] == 1


