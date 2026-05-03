import tkinter as tk
from tkinter import scrolledtext

def show_popup(optimized_code):
    root = tk.Tk()
    root.title("Optimized version of your code")

    root.geometry("700x500")

    # Title label
    label = tk.Label(root, text="🚀 Optimized Code", font=("Arial", 16))
    label.pack(pady=10)

    # Text area
    text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Courier", 10))
    text_area.pack(expand=True, fill="both", padx=10, pady=10)

    text_area.insert(tk.END, optimized_code)

    # Copy button
    def copy_code():
        root.clipboard_clear()
        root.clipboard_append(optimized_code)
        root.update()

    copy_btn = tk.Button(root, text="Copy Code", command=copy_code)
    copy_btn.pack(pady=10)

    root.mainloop()
