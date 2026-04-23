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
        self.last_run = 0
        self.processing_files = set()

    def on_modified(self, event):
        if event.is_directory:
            return

        file_path = event.src_path
        filename = os.path.basename(file_path)

        # ❌ Ignore backup / hidden / temp files
        if (
             filename.endswith(".bak")
            or "_backup" in filename
            or filename.startswith(".")
        ):
            return

        # ❌ Avoid infinite loop
        if file_path in self.processing_files:
            return

        current_time = time.time()

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
