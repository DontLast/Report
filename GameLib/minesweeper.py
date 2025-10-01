import tkinter as tk
from tkinter import messagebox
import random

ROWS = 30
COLS = 30
MINES_COUNT = 100  # количество мин

buttons = []
mines = set()
flags_left = MINES_COUNT
label_flags = None
label_mines = None


class Cell:
    def __init__(self, button, row, col):
        self.button = button
        self.row = row
        self.col = col
        self.is_mine = False
        self.is_open = False
        self.is_flagged = False
        self.neighbor_mines = 0


def place_mines():
    global mines
    mines = set()
    while len(mines) < MINES_COUNT:
        r = random.randint(0, ROWS - 1)
        c = random.randint(0, COLS - 1)
        mines.add((r, c))

    for r, c in mines:
        buttons[r][c].is_mine = True

    # считаем соседние мины
    for r in range(ROWS):
        for c in range(COLS):
            if buttons[r][c].is_mine:
                continue
            count = 0
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < ROWS and 0 <= nc < COLS and buttons[nr][nc].is_mine:
                        count += 1
            buttons[r][c].neighbor_mines = count


def reveal_cell(cell):
    if cell.is_open or cell.is_flagged:
        return
    cell.is_open = True
    if cell.is_mine:
        cell.button.config(text="*", bg="red", state="disabled", disabledforeground="black")
        messagebox.showerror("Игра окончена", "Вы подорвались на мине!")
        new_game()
        return

    cell.button.config(relief=tk.SUNKEN, bg="lightgrey", state="disabled")
    if cell.neighbor_mines > 0:
        # Цвета для цифр 1-8
        colors = {
            1: "blue",
            2: "orange",
            3: "red",
            4: "purple",
            5: "goldenrod",
            6: "cyan",
            7: "pink",
            8: "black"
        }
        cell.button.config(text=str(cell.neighbor_mines),
                           disabledforeground=colors.get(cell.neighbor_mines, "black"))
    else:
        # если пустая — открываем соседей
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                nr, nc = cell.row + dr, cell.col + dc
                if 0 <= nr < ROWS and 0 <= nc < COLS:
                    neighbor = buttons[nr][nc]
                    if not neighbor.is_open:
                        reveal_cell(neighbor)
    check_win()



def toggle_flag(cell):
    global flags_left
    if cell.is_open:
        return
    if cell.is_flagged:
        cell.is_flagged = False
        cell.button.config(text="")
        flags_left += 1
    else:
        if flags_left > 0:
            cell.is_flagged = True
            cell.button.config(text="🚩", fg="red")
            flags_left -= 1
    label_flags.config(text=f"Флаги: {flags_left}")


def check_win():
    for r in range(ROWS):
        for c in range(COLS):
            cell = buttons[r][c]
            if not cell.is_mine and not cell.is_open:
                return
    messagebox.showinfo("Победа!", "Вы нашли все мины!")
    new_game()


def on_left_click(event, cell):
    reveal_cell(cell)


def on_right_click(event, cell):
    toggle_flag(cell)


def new_game():
    global buttons, flags_left
    flags_left = MINES_COUNT
    label_flags.config(text=f"Флаги: {flags_left}")
    for row in range(ROWS):
        for col in range(COLS):
            btn = buttons[row][col].button
            btn.config(text="", relief=tk.RAISED, bg="SystemButtonFace", state="normal")
            buttons[row][col].is_mine = False
            buttons[row][col].is_open = False
            buttons[row][col].is_flagged = False
            buttons[row][col].neighbor_mines = 0
    place_mines()


def start_game():
    global buttons, label_flags, label_mines
    window = tk.Toplevel()
    window.title("Сапёр")

    top_frame = tk.Frame(window)
    top_frame.pack(side=tk.TOP, pady=5)

    label_mines = tk.Label(top_frame, text=f"Мины: {MINES_COUNT}", font=("Arial", 12))
    label_mines.pack(side=tk.LEFT, padx=10)

    label_flags = tk.Label(top_frame, text=f"Флаги: {flags_left}", font=("Arial", 12))
    label_flags.pack(side=tk.LEFT, padx=10)

    btn_restart = tk.Button(top_frame, text="Новая игра", command=new_game)
    btn_restart.pack(side=tk.LEFT, padx=10)

    board_frame = tk.Frame(window)
    board_frame.pack()

    buttons.clear()
    for r in range(ROWS):
        row_buttons = []
        for c in range(COLS):
            btn = tk.Button(board_frame, width=2, height=1)
            btn.grid(row=r, column=c)
            cell = Cell(btn, r, c)
            btn.bind("<Button-1>", lambda e, cell=cell: on_left_click(e, cell))
            btn.bind("<Button-3>", lambda e, cell=cell: on_right_click(e, cell))
            row_buttons.append(cell)
        buttons.append(row_buttons)

    place_mines()
