from file_watcher import start_watching
from config import WATCH_DIRECTORY
import os

def main():
    if not os.path.exists(WATCH_DIRECTORY):
        os.makedirs(WATCH_DIRECTORY)

    start_watching(WATCH_DIRECTORY)

if __name__ == "__main__":
    main()