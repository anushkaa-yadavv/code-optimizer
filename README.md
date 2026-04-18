# ⚡ Real-Time Code Optimization System

## 📌 What this project does
This project is a Python-based real-time code analysis tool that monitors files and automatically analyzes and improves code quality.

---

## 🚀 Features
- Real-time file monitoring (watchdog)
- Code risk analysis (0–100 score)
- Detects:
  - Deep nesting
  - Too many loops
  - Code complexity issues
- Automatic backup before changes
- Code formatting using autopep8

---

## 🧠 Tech Stack
- Python
- watchdog
- AST (Abstract Syntax Tree)
- autopep8
- Linux environment

---

## 📂 Project Structure
- main.py → starts system
- file_watcher.py → monitors file changes
- analyzer.py → calculates risk score
- optimizer.py → improves code
- utils.py → helper functions
- watched_dir → files to test

---

## ▶️ How to run

```bash
source venv/bin/activate
python main.py

