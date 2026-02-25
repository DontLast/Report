# launcher.py
import threading
import webbrowser
import time
from app import app

def open_browser():
    """Открывает браузер через небольшую задержку, чтобы сервер успел запуститься."""
    time.sleep(1.5)
    webbrowser.open("http://127.0.0.1:5000")

if __name__ == "__main__":
    # Запускаем браузер в фоне
    threading.Thread(target=open_browser, daemon=True).start()
    # Запускаем сервер (однопоточный режим для совместимости с PyInstaller)
    app.run(host="127.0.0.1", port=5000, debug=False, threaded=False)