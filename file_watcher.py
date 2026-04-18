from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

from analyzer import CodeAnalyzer
from optimizer import CodeOptimizer
from utils import read_file, write_file, create_backup
from config import SUPPORTED_EXTENSIONS, RISK_THRESHOLD


class CodeEventHandler(FileSystemEventHandler):

    def __init__(self):
        self.last_run = 0

    def on_modified(self, event):
        if event.is_directory:
            return

        current_time = time.time()

        # Debounce (avoid multiple triggers)
        if current_time - self.last_run < 1:
            return

        self.last_run = current_time

        file_path = event.src_path

        if not any(file_path.endswith(ext) for ext in SUPPORTED_EXTENSIONS):
            return

        print(f"\n📄 File changed: {file_path}")

        try:
            code = read_file(file_path)

            analyzer = CodeAnalyzer(code)
            result = analyzer.analyze()

            print(f"⚠️ Risk Score: {result['risk_score']}")
            print("Issues:")
            for issue in result["issues"]:
                print(f" - {issue}")

            if result["risk_score"] > RISK_THRESHOLD:
                print("🚀 Optimization triggered...")

                backup_path = create_backup(file_path)
                print(f"Backup created: {backup_path}")

                optimizer = CodeOptimizer(code)
                new_code, status = optimizer.optimize()

                if optimizer.validate_syntax(new_code):
                    write_file(file_path, new_code)
                    print(f"✅ {status}")
                else:
                    print("❌ Optimization skipped (invalid syntax)")
            else:
                print("✔ No optimization needed")

        except Exception as e:
            print(f"Error: {e}")


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