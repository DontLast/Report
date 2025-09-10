import subprocess
import sys
import os
import webbrowser
import time
from pathlib import Path


def check_requirements():
    """Проверяем установлены ли необходимые пакеты"""
    try:
        import fastapi
        import uvicorn
        import sqlalchemy
        import pydantic
        print("Все зависимости установлены")
        return True
    except ImportError as e:
        print(f"Не установлены зависимости: {e}")
        print("Установите зависимости командой:")
        print("pip install fastapi uvicorn sqlalchemy pydantic python-multipart")
        return False


def run_backend():
    """Запуск FastAPI сервера"""
    backend_dir = Path("backend")
    os.chdir(backend_dir)

    print("Запускаем FastAPI сервер на http://localhost:8000")
    try:
        # Запускаем uvicorn
        subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"])
        return True
    except Exception as e:
        print(f"Ошибка запуска бэкенда: {e}")
        return False
    finally:
        os.chdir("..")


def serve_frontend():
    """Запуск простого HTTP сервера для фронтенда"""
    frontend_dir = Path("frontend")

    print("Запускаем HTTP сервер для фронтенда на http://localhost:8080")
    try:
        # Используем встроенный HTTP сервер Python
        subprocess.Popen([sys.executable, "-m", "http.server", "8080", "-d", str(frontend_dir)])
        return True
    except Exception as e:
        print(f"Ошибка запуска фронтенда: {e}")
        return False


def main():
    print("=" * 50)
    print("Запуск приложения регистрации")
    print("=" * 50)

    # Проверяем зависимости
    if not check_requirements():
        print("Пожалуйста, установите зависимости вручную")
        return

    # Запускаем бэкенд
    if not run_backend():
        return

    # Даем время серверу запуститься
    time.sleep(3)

    # Запускаем фронтенд
    if not serve_frontend():
        return

    # Даем время серверам запуститься
    time.sleep(2)

    # Открываем браузер
    print("Открываем браузер...")
    webbrowser.open("http://localhost:8080")

    print("\n" + "=" * 50)
    print("Приложение запущено!")
    print("Фронтенд: http://localhost:8080")
    print("Бэкенд:    http://localhost:8000")
    print("Документация API: http://localhost:8000/docs")
    print("Для остановки нажмите Ctrl+C в этом окне")
    print("=" * 50)

    try:
        # Держим программу активной
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nОстанавливаем приложение...")


if __name__ == "__main__":
    main()