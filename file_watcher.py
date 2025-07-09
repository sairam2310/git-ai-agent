import os
import time
import asyncio
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import global_state
from file_change_handler import file_change_queue

# Optional: Delay threshold in seconds to avoid rapid duplicate queuing
DEBOUNCE_DELAY = 1.0  # 1 second

def start_file_watcher(loop, path="."):
    last_queued_time = {}

    class FileChangeHandler(FileSystemEventHandler):
        def on_any_event(self, event):
            try:
                if event.event_type in ["modified", "created", "deleted"] and not event.is_directory:
                    changed_file = os.path.basename(event.src_path)
                    current_time = time.time()

                    # ✅ Debounce: Only trigger if last change was long ago
                    if (changed_file not in last_queued_time) or (current_time - last_queued_time[changed_file]) > DEBOUNCE_DELAY:
                        last_queued_time[changed_file] = current_time

                        global_state.UNCOMMITTED_CHANGES = True
                        global_state.CHANGED_FILES.add(changed_file)

                        print(f"📝 Detected file change: {changed_file}")

                        # Push updated list (only once)
                        asyncio.run_coroutine_threadsafe(
                            file_change_queue.put(list(global_state.CHANGED_FILES)),
                            loop
                        )
                        print("📬 Queued files:", list(global_state.CHANGED_FILES))

            except Exception as e:
                print(f"⚠️ Error in file watcher: {e}")

    observer = Observer()
    observer.schedule(FileChangeHandler(), path=path, recursive=True)
    observer.start()

    print(f"📡 File watcher started on path: {os.path.abspath(path)}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("🛑 Stopping file watcher.")
        observer.stop()
    observer.join()


