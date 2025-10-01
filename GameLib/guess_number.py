import tkinter as tk
import random

secret_number = None
attempts = 0


def new_game(label_result):
    global secret_number, attempts
    secret_number = random.randint(1, 100)
    attempts = 0
    label_result.config(text="Я загадал число от 1 до 100.\nПопробуй угадать!")


def check_guess(entry, label_result):
    global secret_number, attempts
    try:
        guess = int(entry.get())
        attempts += 1
        if guess < secret_number:
            label_result.config(text=f"{guess} — Мало! Попробуй больше.")
        elif guess > secret_number:
            label_result.config(text=f"{guess} — Много! Попробуй меньше.")
        else:
            label_result.config(text=f"Поздравляю! Ты угадал {guess} за {attempts} попыток!")
    except ValueError:
        label_result.config(text="Введи число!")


def start_game():
    window = tk.Toplevel()
    window.title("Угадай число")
    window.geometry("400x300")

    label_title = tk.Label(window, text="Игра: Угадай число", font=("Arial", 14))
    label_title.pack(pady=10)

    label_result = tk.Label(window, text="", font=("Arial", 12))
    label_result.pack(pady=10)

    entry = tk.Entry(window, font=("Arial", 12))
    entry.pack(pady=5)

    btn_check = tk.Button(window, text="Проверить",
                          command=lambda: check_guess(entry, label_result))
    btn_check.pack(pady=5)

    btn_new = tk.Button(window, text="Новая игра",
                        command=lambda: new_game(label_result))
    btn_new.pack(pady=5)

    btn_close = tk.Button(window, text="Закрыть", command=window.destroy)
    btn_close.pack(pady=10)

    # запуск первой игры
    new_game(label_result)
