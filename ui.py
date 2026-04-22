import tkinter as tk
from tkinter import filedialog
import threading

from file_watcher import start_watching

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Code Optimizer")

        self.label = tk.Label(root, text="Select folder to watch")
        self.label.pack(pady=10)

        self.path_entry = tk.Entry(root, width=50)
        self.path_entry.pack(pady=5)

        self.browse_btn = tk.Button(root, text="Browse", command=self.browse)
        self.browse_btn.pack(pady=5)

        self.start_btn = tk.Button(root, text="Start Watching", command=self.start)
        self.start_btn.pack(pady=10)

        self.log_box = tk.Text(root, height=15, width=70)
        self.log_box.pack(pady=10)

    def browse(self):
        folder = filedialog.askdirectory()
        self.path_entry.delete(0, tk.END)
        self.path_entry.insert(0, folder)

    def start(self):
        path = self.path_entry.get()
        self.log("👀 Watching started...")

        thread = threading.Thread(target=start_watching, args=(path,))
        thread.daemon = True
        thread.start()
    def log(self, message):
        self.log_box.insert(tk.END, message + "\n")
        self.log_box.see(tk.END)

root = tk.Tk()
app = App(root)
root.mainloop()
