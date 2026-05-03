import threading
import queue
from file_watcher import start_watching
from ui_popup import show_popup

# 🔥 Queue for communication
popup_queue = queue.Queue()


def watcher_thread():
    start_watching("./watched_dir", popup_queue)


def ui_loop():
    while True:
        code = popup_queue.get()
        if code:
            show_popup(code)


if __name__ == "__main__":
    # watcher runs in background
    t = threading.Thread(target=watcher_thread, daemon=True)
    t.start()

    # UI runs in main thread
    ui_loop()
