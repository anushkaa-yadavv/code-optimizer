from ui_popup import show_popup
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import os

from analyzer import CodeAnalyzer
from optimizer import CodeOptimizer
from utils import read_file, write_file, create_backup
from config import SUPPORTED_EXTENSIONS, RISK_THRESHOLD


class CodeEventHandler(FileSystemEventHandler):

    def __init__(self):
        self.last_run = {}
        self.processing_files = set()

    def should_ignore(self, file_path):
        # Ignore temp / backup / optimized files
        if file_path.endswith(".bak") or "_backup" in file_path:
            return True
        if file_path.endswith("~") or ".swp" in file_path:
            return True
        if "_optimized.py" in file_path:
            return True
        return False

    def process(self, event):
        if event.is_directory:
            return

        file_path = event.src_path

        if self.should_ignore(file_path):
            return

        if not any(file_path.endswith(ext) for ext in SUPPORTED_EXTENSIONS):
            return

        if file_path in self.processing_files:
            return

        # 🔥 debounce
        current_time = time.time()
        if file_path in self.last_run and current_time - self.last_run[file_path] < 1:
            return
        self.last_run[file_path] = current_time

        print(f"\n📄 File changed: {file_path}")

        try:
            self.processing_files.add(file_path)

            code = read_file(file_path)

            analyzer = CodeAnalyzer(code)
            result = analyzer.analyze()

            print(f"⚠️ Risk Score: {result['risk_score']}")
            print(f"🎯 Threshold: {RISK_THRESHOLD}")

            if result["issues"]:
                print("Issues:")
                for issue in result["issues"]:
                    print(f" - {issue}")
            else:
                print("✔ No issues detected")

            if result["risk_score"] >= RISK_THRESHOLD:
                print("🚀 Optimization triggered...")

                # backup
                backup_path = file_path + ".bak"
                if not os.path.exists(backup_path):
                    create_backup(file_path)
                    print("📦 Backup created")
                else:
                    print("📦 Backup exists")

                optimizer = CodeOptimizer(code)
                new_code, status = optimizer.optimize()

                # 🔥 skip if no real change
                if new_code.strip() == code.strip():
                    print("⚠️ No changes made")
                    return

                if optimizer.validate_syntax(new_code):
                    # 🔥 SAVE AS NEW FILE (NO LOOP)
                    optimized_path = file_path.replace(".py", "_optimized.py")
                    write_file(optimized_path, new_code)

                    print(f"✅ {status}")
                    print(f"📁 Saved: {optimized_path}")

                    # 🔥 SHOW UI POPUP
                    show_popup(new_code)

                else:
                    print("❌ Invalid optimized code")

            else:
                print("✔ No optimization needed")

        except Exception as e:
            print(f"❌ Error: {e}")

        finally:
            time.sleep(0.5)
            self.processing_files.discard(file_path)

    def on_modified(self, event):
        self.process(event)

    def on_created(self, event):
        self.process(event)

    def on_moved(self, event):
        self.process(event)


def start_watching(directory):
    observer = Observer()
    observer.schedule(CodeEventHandler(), path=directory, recursive=True)

    observer.start()
    print(f"👀 Watching: {directory}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()        current_time = time.time()

        # 🔥 Better debounce (slow spam fix)
        if current_time - self.last_run < 2:
            return

      

        # ❌ Only supported files
        if not any(file_path.endswith(ext) for ext in SUPPORTED_EXTENSIONS):
            return

        print(f"\n📄 File changed: {file_path}")

        try:
            self.processing_files.add(file_path)

            code = read_file(file_path)

            # ❌ Ignore very small files
            if len(code.strip()) < 10:
                print("⚠️ Skipped (file too small)")
                return

            analyzer = CodeAnalyzer(code)
            result = analyzer.analyze()

            risk = result.get("risk_score", 0)

            print(f"⚠️ Risk Score: {risk}")
            print(f"🎯 Threshold: {RISK_THRESHOLD}")  # 🔥 DEBUG FIX

            print("Issues:")
            for issue in result.get("issues", []):
                print(f" - {issue}")

            # 🔥 FIXED CONDITION (>= instead of >)
            if risk >= RISK_THRESHOLD:
                print("🚀 Optimization triggered...")

                # ✅ Create backup only once
                backup_path = file_path + ".bak"
                if not os.path.exists(backup_path):
                    create_backup(file_path)
                    print(f"📦 Backup created: {backup_path}")
                else:
                    print("📦 Backup already exists")

                optimizer = CodeOptimizer(code)
                new_code, status = optimizer.optimize()

                if optimizer.validate_syntax(new_code):
                    if new_code.strip() != code.strip():
                        write_file(file_path, new_code)
                        print(f"✅ {status}")
                    else:  
                        print("✔ No optimization needed")

                else:
                    print("❌ Optimization failed (syntax error), no changes made")

        except Exception as e:
            print(f"❌ Error: {e}")

        finally:
            self.last_run = time.time()
            self.processing_files.discard(file_path)


def start_watching(directory):
    observer = Observer()
    observer.schedule(CodeEventHandler(), directory, recursive=True)

    observer.start()
    print(f"👀 Watching: {directory}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
