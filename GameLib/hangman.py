import tkinter as tk
from tkinter import messagebox
import random

# Словарь слов (можно дополнять)
words = ["python", "игра", "программа", "компьютер", "библиотека", "окно", "клавиатура", "разработка", "алгоритм"]

secret_word = ""
guessed_letters = []
mistakes = 0
max_mistakes = 6

label_word = None
label_info = None
label_used = None
canvas = None

# координаты для рисования (на canvas размером 300x250)
# Галерея рисуется сразу, фигурка — по ошибкам
def draw_gallows():
    canvas.delete("all")
    # основание
    canvas.create_line(20, 230, 180, 230, width=4)        # база
    canvas.create_line(60, 230, 60, 30, width=4)          # стойка
    canvas.create_line(60, 30, 140, 30, width=4)          # перекладина
    canvas.create_line(140, 30, 140, 60, width=3)         # верёвка

def draw_head():
    # голова (круг)
    canvas.create_oval(120, 60, 160, 100, width=3)

def draw_body():
    # тело
    canvas.create_line(140, 100, 140, 160, width=3)

def draw_left_arm():
    canvas.create_line(140, 110, 115, 140, width=3)

def draw_right_arm():
    canvas.create_line(140, 110, 165, 140, width=3)

def draw_left_leg():
    canvas.create_line(140, 160, 115, 195, width=3)

def draw_right_leg():
    canvas.create_line(140, 160, 165, 195, width=3)

draw_steps = [draw_head, draw_body, draw_left_arm, draw_right_arm, draw_left_leg, draw_right_leg]

def new_game():
    global secret_word, guessed_letters, mistakes
    secret_word = random.choice(words).upper()
    guessed_letters = []
    mistakes = 0
    draw_gallows()
    update_word_display()
    update_info()
    update_used_display()

def update_word_display():
    display = " ".join([letter if letter in guessed_letters else "_" for letter in secret_word])
    label_word.config(text=display)

def update_info():
    label_info.config(text=f"Ошибки: {mistakes}/{max_mistakes}")

def update_used_display():
    used = ", ".join(guessed_letters) if guessed_letters else "—"
    label_used.config(text=f"Введённые буквы: {used}")

def guess_letter(entry):
    global mistakes
    letter = entry.get().strip().upper()
    entry.delete(0, tk.END)

    if not letter or not letter.isalpha() or len(letter) != 1:
        messagebox.showwarning("Ошибка", "Введите одну букву (А-Я или A-Z).")
        return

    if letter in guessed_letters:
        messagebox.showinfo("Уже вводили", f"Буква '{letter}' уже вводилась.")
        return

    guessed_letters.append(letter)
    update_used_display()

    if letter in secret_word:
        update_word_display()
        # проверим победу
        if all(l in guessed_letters for l in secret_word):
            update_word_display()
            messagebox.showinfo("Победа!", f"Поздравляю! Слово: {secret_word}")
            new_game()
    else:
        # ошибка — рисуем следующую часть
        if mistakes < max_mistakes:
            draw_steps[mistakes]()  # mistakes ещё старое значение: 0..5 -> рисуем соответствующий шаг
        mistakes += 1
        update_info()
        if mistakes >= max_mistakes:
            # показываем проигрыш и полное слово, затем новая игра
            messagebox.showerror("Проигрыш", f"Ты проиграл! Загаданное слово: {secret_word}")
            new_game()

def start_game():
    global label_word, label_info, label_used, canvas
    window = tk.Toplevel()
    window.title("Висельник")
    window.geometry("650x330")  # оставим побольше пространства для canvas и управления

    top_frame = tk.Frame(window)
    top_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10)

    right_frame = tk.Frame(window)
    right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=10, pady=10)

    # Canvas для рисования виселицы
    canvas = tk.Canvas(top_frame, width=300, height=250, bg="white")
    canvas.pack()

    # Игровая панель справа
    tk.Label(right_frame, text="Игра: Висельник", font=("Arial", 14)).pack(pady=5)

    label_word = tk.Label(right_frame, text="", font=("Consolas", 20))
    label_word.pack(pady=10)

    label_info = tk.Label(right_frame, text="", font=("Arial", 12))
    label_info.pack(pady=5)

    label_used = tk.Label(right_frame, text="", font=("Arial", 10))
    label_used.pack(pady=5)

    entry = tk.Entry(right_frame, font=("Arial", 14), width=6)
    entry.pack(pady=5)
    entry.focus_set()

    btn_guess = tk.Button(right_frame, text="Проверить букву", width=15, command=lambda: guess_letter(entry))
    btn_guess.pack(pady=5)

    btn_new = tk.Button(right_frame, text="Новая игра", width=15, command=new_game)
    btn_new.pack(pady=5)

    btn_close = tk.Button(right_frame, text="Закрыть", width=15, command=window.destroy)
    btn_close.pack(pady=5)

    # Подсказка: можно угадывать целиком слово, если ввести больше 1 буквы:
    def guess_whole_word(event=None):
        nonlocal entry
        text = entry.get().strip().upper()
        entry.delete(0, tk.END)
        if not text:
            return
        # если ввели больше 1 символа — считаем это попыткой угадать слово целиком
        if len(text) > 1:
            if text == secret_word:
                messagebox.showinfo("Победа!", f"Правильно! Слово: {secret_word}")
                new_game()
            else:
                # целиком неверно — считаем как одна ошибка + рисунок
                global mistakes
                if mistakes < max_mistakes:
                    draw_steps[mistakes]()
                mistakes += 1
                update_info()
                update_used_display()
                if mistakes >= max_mistakes:
                    messagebox.showerror("Проигрыш", f"Ты проиграл! Загаданное слово: {secret_word}")
                    new_game()

    # Привязка Enter к проверке буквы / слова
    entry.bind("<Return>", lambda e: guess_letter(entry) if len(entry.get().strip()) == 1 else guess_whole_word())

    # Запуск новой игры при открытии окна
    new_game()
