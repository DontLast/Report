import tkinter as tk
from tkinter import messagebox

current_player = "X"
buttons = []


def new_game():
    global current_player, buttons
    current_player = "X"
    for row in buttons:
        for btn in row:
            btn.config(text="", state="normal")


def check_winner():
    # Проверка строк
    for row in buttons:
        if row[0]["text"] == row[1]["text"] == row[2]["text"] != "":
            return row[0]["text"]

    # Проверка столбцов
    for col in range(3):
        if buttons[0][col]["text"] == buttons[1][col]["text"] == buttons[2][col]["text"] != "":
            return buttons[0][col]["text"]

    # Проверка диагоналей
    if buttons[0][0]["text"] == buttons[1][1]["text"] == buttons[2][2]["text"] != "":
        return buttons[0][0]["text"]
    if buttons[0][2]["text"] == buttons[1][1]["text"] == buttons[2][0]["text"] != "":
        return buttons[0][2]["text"]

    # Проверка на ничью
    if all(btn["text"] != "" for row in buttons for btn in row):
        return "Ничья"

    return None


def on_click(row, col):
    global current_player
    if buttons[row][col]["text"] == "":
        buttons[row][col]["text"] = current_player
        winner = check_winner()
        if winner:
            if winner == "Ничья":
                messagebox.showinfo("Игра окончена", "Ничья!")
            else:
                messagebox.showinfo("Игра окончена", f"Победил {winner}!")
            new_game()
        else:
            current_player = "O" if current_player == "X" else "X"


def start_game():
    global buttons
    window = tk.Toplevel()
    window.title("Крестики-нолики")
    window.geometry("320x400")

    label = tk.Label(window, text="Крестики-нолики", font=("Arial", 14))
    label.pack(pady=10)

    frame = tk.Frame(window)
    frame.pack()

    buttons = []
    for row in range(3):
        row_buttons = []
        for col in range(3):
            btn = tk.Button(frame, text="", width=8, height=4,
                            font=("Arial", 14),
                            command=lambda r=row, c=col: on_click(r, c))
            btn.grid(row=row, column=col)
            row_buttons.append(btn)
        buttons.append(row_buttons)

    tk.Button(window, text="Новая игра", command=new_game).pack(pady=10)
    tk.Button(window, text="Закрыть", command=window.destroy).pack(pady=5)

    new_game()
