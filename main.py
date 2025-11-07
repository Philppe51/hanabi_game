"""
Point d'entrée principal pour le jeu Hanabi en mode interface graphique (Tkinter).
"""

from hanabi.game import HanabiGame, ClueType, Color
from hanabi.gui import HanabiGUI

def main():
    # Crée une partie avec 2 à 4 joueurs (par défaut : 2 joueurs)
    player_names = ["Joueur 1", "Joueur 2"]  # Vous pouvez modifier cette liste
    game = HanabiGame(player_names)

    # Lance l'interface graphique
    gui = HanabiGUI(game)
    gui.run()

if __name__ == "__main__":
    main()