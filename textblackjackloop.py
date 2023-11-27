"""
This is a simple blackjack game, created using the tkinter library.

Input:
    User mouse


Output:
    Blackjack game


References:
 * https://stackoverflow.com/questions/61639278/to-detect-button-press-in-python-tkinter-module
 * https://www.geeksforgeeks.org/blackjack-console-game-using-python/


CIS 216 Team 4:
Timothy El Moughayar
Frank Boxenbaum
Tyler Reynolds

"""

import tkinter as tk
from tkinter import messagebox
import random


class BlackjackGame:
    """Creates blackjack game class"""
    def __init__(self, master):
        """Initializes deck of cards and deals hands to player and dealer."""
        self.master = master
        self.master.geometry("800x600")
        self.master.title("Blackjack Game")
        self.master.configure(background="green")

        self.deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11] * 4
        random.shuffle(self.deck)

        self.player_hand = [self.deck.pop(), self.deck.pop()]
        self.dealer_hand = [self.deck.pop(), self.deck.pop()]

        self.player_bust = False
        self.dealer_bust = False
        self.player_stand = False

        self.create_widgets()

    def create_widgets(self):
        """Creates the on screen text and buttons."""
        self.dealer_frame = tk.LabelFrame(self.master, text="Dealer", bd=0, height=100, width=200)
        self.dealer_frame.grid(row=0, column=0, padx=(20, 100), ipadx=20)

        self.player_frame = tk.LabelFrame(self.master, text="Player", bd=0, height=100, width=200)
        self.player_frame.grid(row=0, column=1, padx=0, ipadx=20)

        self.quit_button = tk.Button(self.master, text="Quit", command=self.master.destroy)
        self.quit_button.grid(row=2, column=0, padx=(20, 100), pady=30, sticky=tk.W)

        self.hit_button = tk.Button(self.master, text="Hit", command=self.hit)
        self.hit_button.grid(row=2, column=1, padx=(0, 90), pady=30, sticky=tk.W+tk.E)

        self.stand_button = tk.Button(self.master, text="Stand", command=self.stand)
        self.stand_button.grid(row=2, column=2, sticky=tk.W+tk.E, padx=(0, 100), pady=30)

        self.update_display()

    def calculate_hand_value(self, hand):
        """Calculate the value of the player and dealer's hands."""
        value = sum(hand)
        num_aces = hand.count(11)

        while value > 21 and num_aces:
            value -= 10
            num_aces -= 1

        return value

    def update_display(self):
        """Updates the game area display with the current cards and decides the game outcome."""
        player_value = self.calculate_hand_value(self.player_hand)
        dealer_value = self.calculate_hand_value(self.dealer_hand)

        dealer_text = f"Dealer's Hand: {self.dealer_hand} ({dealer_value})"
        player_text = f"Player's Hand: {self.player_hand} ({player_value})"

        self.dealer_frame.config(text=dealer_text)
        self.player_frame.config(text=player_text)

        if player_value > 21:
            self.player_bust = True
            self.end_game("Player busts! Dealer wins.")
        elif self.dealer_bust:
            self.end_game("Dealer busts! Player wins.")
        elif player_value == dealer_value == 21:
            self.end_game("It's a tie! Both have Blackjack!")
        elif player_value == 21:
            self.end_game("Player wins with Blackjack!")
        elif dealer_value == 21:
            self.end_game("Dealer wins with Blackjack!")
        elif player_value > dealer_value and self.player_stand is True:
            self.end_game("Player wins!")
        elif player_value < dealer_value and self.player_stand is True:
            self.end_game("Dealer wins!")
        elif player_value == dealer_value and self.player_stand is True:
            self.end_game("Tie!")

    def end_game(self, message):
        """Displays the results of the game round and asks if the user want to play again or quit."""
        messagebox.showinfo("Results", message)
        answer = messagebox.askyesno(title="Game Over", message="Do you want to play again?")
        if answer:
            self.player_hand = 0
            self.dealer_hand = 0
            self.player_frame.config(text="")
            self.dealer_frame.config(text="")
            BlackjackGame(self.master)
        else:
            messagebox.showinfo("Goodbye", message="Thanks for playing!")
            self.master.destroy()

    def hit(self):
        """Adds another card from the deck to the player's hand."""
        self.player_hand.append(self.deck.pop())
        self.update_display()

    def stand(self):
        """The player declines to draw another card and the game progresses to the outcome."""
        while self.calculate_hand_value(self.dealer_hand) < 17:
            self.dealer_hand.append(self.deck.pop())

        self.dealer_bust = self.calculate_hand_value(self.dealer_hand) > 21
        self.player_stand = True
        self.update_display()


"""Creates window, launches game, and runs loops the GUI."""
if __name__ == "__main__":
    root = tk.Tk()
    game = BlackjackGame(root)
    root.mainloop()