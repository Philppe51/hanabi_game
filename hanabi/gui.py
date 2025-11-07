import tkinter as tk
from tkinter import messagebox, simpledialog
from typing import List
from hanabi.game import HanabiGame, ClueType, Color

class HanabiGUI:
    def __init__(self, game: HanabiGame):
        self.game = game
        self.window = tk.Tk()
        self.window.title("Hanabi")
        self.current_player_index = 0

        # Frames pour chaque joueur
        self.player_frames = []
        for i, player in enumerate(self.game.players):
            frame = tk.LabelFrame(self.window, text=f"{player.name} (Joueur {i + 1})")
            frame.pack(pady=5, padx=10, fill="x")
            self.player_frames.append(frame)

        # Frame pour le plateau (cartes jouées, défaussées, etc.)
        self.board_frame = tk.LabelFrame(self.window, text="Plateau de jeu")
        self.board_frame.pack(pady=10, padx=10, fill="x")

        # Frame pour les actions
        self.action_frame = tk.LabelFrame(self.window, text="Actions")
        self.action_frame.pack(pady=10, padx=10, fill="x")

        # Frame pour l'historique des indices
        self.clues_frame = tk.LabelFrame(self.window, text="Historique des indices")
        self.clues_frame.pack(pady=10, padx=10, fill="x")

        # Bouton pour passer au tour suivant
        self.next_turn_button = tk.Button(self.action_frame, text="Terminer le tour", command=self.next_turn)
        self.next_turn_button.grid(row=0, column=3, padx=5)

        # Initialise l'affichage
        self.update_display()

    def update_display(self):
        """Met à jour l'affichage du jeu."""
        # Efface les anciens widgets
        for frame in self.player_frames:
            for widget in frame.winfo_children():
                widget.destroy()
        for widget in self.board_frame.winfo_children():
            widget.destroy()
        for widget in self.action_frame.winfo_children():
            if widget != self.next_turn_button:
                widget.destroy()
        for widget in self.clues_frame.winfo_children():
            widget.destroy()

        # Affiche les cartes de chaque joueur
        for i, player in enumerate(self.game.players):
            frame = self.player_frames[i]
            is_current_player = (i == self.current_player_index)

            for j, card in enumerate(player.hand):
                card_frame = tk.Frame(frame, bd=2, relief="groove")
                card_frame.grid(row=0, column=j, padx=2)

                # Affiche la carte cachée ou visible selon le joueur
                if is_current_player:
                    tk.Label(card_frame, text="[Carte]", width=8, height=4, bg="lightgrey").pack()
                else:
                    tk.Label(card_frame, text=f"{card.color.name}\n{card.value}", width=8, height=4, bg="white").pack()

                # Boutons pour jouer/défausser (uniquement pour le joueur actuel)
                if is_current_player:
                    tk.Button(card_frame, text="Jouer", command=lambda idx=j: self.play_card(idx)).pack(side="left", padx=1)
                    tk.Button(card_frame, text="Défausser", command=lambda idx=j: self.discard_card(idx)).pack(side="right", padx=1)

                # Affiche les indices sur cette carte (si disponibles)
                if hasattr(player, 'clues') and j in player.clues:
                    for clue_type, clue_value in player.clues[j]:
                        clue_text = f"{clue_type}: {clue_value}"
                        tk.Label(card_frame, text=clue_text, fg="red", font=("Arial", 8)).pack()

        # Affiche les cartes jouées et défaussées
        played_cards_text = ", ".join([f"{color.name}: {value}" for color, value in self.game.played_cards.items()])
        tk.Label(self.board_frame, text=f"Cartes jouées: {played_cards_text}").grid(row=0, column=0, padx=5)
        tk.Label(self.board_frame, text=f"Cartes défaussées: {len(self.game.discard_pile)}").grid(row=0, column=1, padx=5)
        tk.Label(self.board_frame, text=f"Indices restants: {self.game.clues_available}").grid(row=0, column=2, padx=5)
        tk.Label(self.board_frame, text=f"Vies restantes: {self.game.lives}").grid(row=0, column=3, padx=5)

        # Boutons pour donner un indice (choix du joueur cible)
        tk.Label(self.action_frame, text="Donner un indice à:").grid(row=1, column=0, pady=5)
        for i, player in enumerate(self.game.players):
            if i != self.current_player_index:  # On ne peut pas se donner un indice à soi-même
                tk.Button(self.action_frame, text=player.name,
                          command=lambda idx=i: self.choose_clue_type(idx)).grid(row=1, column=i+1, padx=5)

        # Affiche l'historique des indices
        for i, clue in enumerate(self.game.clues_history):
            giver = self.game.players[clue.giver_index].name
            receiver = self.game.players[clue.receiver_index].name
            clue_desc = f"{clue.clue_type.name}: {clue.value if clue.clue_type == ClueType.VALUE else clue.color.name}"
            tk.Label(self.clues_frame, text=f"Tour {clue.turn}: {giver} → {receiver}: {clue_desc}").grid(row=i, column=0, sticky="w")

    def choose_clue_type(self, target_player_index: int):
        """Ouvre une fenêtre pour choisir le type d'indice à donner."""
        clue_window = tk.Toplevel(self.window)
        clue_window.title("Choisir un indice")

        tk.Label(clue_window, text="Type d'indice:").pack(pady=5)

        # Boutons pour choisir le type d'indice
        tk.Button(clue_window, text="Indice de couleur",
                  command=lambda: self.choose_clue_value(ClueType.COLOR, target_player_index, clue_window)).pack(pady=2)
        tk.Button(clue_window, text="Indice de valeur",
                  command=lambda: self.choose_clue_value(ClueType.VALUE, target_player_index, clue_window)).pack(pady=2)

    def choose_clue_value(self, clue_type: ClueType, target_player_index: int, window: tk.Toplevel):
        """Ouvre une fenêtre pour choisir la valeur de l'indice."""
        window.destroy()

        value_window = tk.Toplevel(self.window)
        value_window.title("Choisir la valeur de l'indice")

        if clue_type == ClueType.COLOR:
            tk.Label(value_window, text="Choisir une couleur:").pack(pady=5)
            for color in Color:
                tk.Button(value_window, text=color.name,
                          command=lambda c=color: self.give_clue(clue_type, target_player_index, color=c, window=value_window)).pack(pady=2)
        else:
            tk.Label(value_window, text="Choisir une valeur:").pack(pady=5)
            for value in range(1, 6):
                tk.Button(value_window, text=str(value),
                          command=lambda v=str(value): self.give_clue(clue_type, target_player_index, value=v, window=value_window)).pack(pady=2)

    def give_clue(self, clue_type: ClueType, target_player_index: int, color: Color = None, value: str = None, window: tk.Toplevel = None):
        """Donne un indice au joueur cible."""
        if window:
            window.destroy()

        if self.game.give_clue(self.current_player_index, target_player_index, clue_type, value, color):
            messagebox.showinfo("Résultat", "Indice donné avec succès.")
        else:
            messagebox.showinfo("Résultat", "Plus d'indices disponibles.")
        self.update_display()

    def play_card(self, card_index: int):
        """Joue la carte à l'index donné."""
        success = self.game.play_card(self.current_player_index, card_index)
        if success:
            message = "Carte jouée avec succès !"
            # Pioche une nouvelle carte
            if self.game.deck.cards:
                new_card = self.game.deck.draw()
                self.game.players[self.current_player_index].add_card(new_card)
        else:
            message = "Carte non jouable. Vie perdue."
        messagebox.showinfo("Résultat", message)
        self.update_display()

    def discard_card(self, card_index: int):
        """Défausse la carte à l'index donné."""
        self.game.discard_card(self.current_player_index, card_index)
        messagebox.showinfo("Résultat", "Carte défaussée. Un indice a été regagné.")
        # Pioche une nouvelle carte
        if self.game.deck.cards:
            new_card = self.game.deck.draw()
            self.game.players[self.current_player_index].add_card(new_card)
        self.update_display()

    def next_turn(self):
        """Passe au joueur suivant."""
        self.current_player_index = (self.current_player_index + 1) % len(self.game.players)
        messagebox.showinfo("Tour suivant", f"C'est au tour de {self.game.players[self.current_player_index].name}.")
        self.update_display()

    def run(self):
        """Lance l'interface graphique."""
        self.window.mainloop()
