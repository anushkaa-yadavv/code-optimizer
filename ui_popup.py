import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import threading
import queue

popup_queue = queue.Queue()


def popup_worker():
    while True:
        code = popup_queue.get()

        root = tk.Tk()
        root.title("Optimized Code")

        text = ScrolledText(root, wrap=tk.WORD, width=100, height=30)
        text.pack(padx=10, pady=10)
        text.insert(tk.END, code)

        def copy_code():
            root.clipboard_clear()
            root.clipboard_append(code)

        btn = tk.Button(root, text="Copy Code", command=copy_code)
        btn.pack(pady=5)

        root.mainloop()


def start_ui_loop():
    t = threading.Thread(target=popup_worker, daemon=True)
    t.start()


def show_popup(code):
    popup_queue.put(code)
