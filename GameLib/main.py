import tkinter as tk
from tkinter import messagebox
import tic_tac_toe
import guess_number
import minesweeper
import hangman


def open_tic_tac_toe():
    tic_tac_toe.start_game()


def open_guess_number():
    guess_number.start_game()


def open_minesweeper():
    minesweeper.start_game()


def open_hangman():
    hangman.start_game()


def main():
    root = tk.Tk()
    root.title("Библиотека игр")
    root.geometry("300x300")

    tk.Label(root, text="Выберите игру:", font=("Arial", 14)).pack(pady=20)

    tk.Button(root, text="Крестики-нолики", width=20, height=2, command=open_tic_tac_toe).pack(pady=5)
    tk.Button(root, text="Угадай число", width=20, height=2, command=open_guess_number).pack(pady=5)
    tk.Button(root, text="Сапёр", width=20, height=2, command=open_minesweeper).pack(pady=5)
    tk.Button(root, text="Висельник", width=20, height=2, command=open_hangman).pack(pady=5)

    root.mainloop()


if __name__ == "__main__":
    main()
