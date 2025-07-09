import asyncio

# This queue will be used by the file watcher thread to push changes
file_change_queue = asyncio.Queue()



# Use get_nowait to avoid blocking


