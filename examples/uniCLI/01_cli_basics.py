"""DuraPy Examples - UniCLI basics"""

from durapy.uniCLI import console_print, console_msg, clear_terminal, Console

# Simple colored messages
print(console_msg("System", "green", "Initialization complete", "white"))
print(console_msg("Warning", "yellow", "Low battery detected", "orange"))
print(console_msg("Error", "red", "Connection failed", "white"))

# console_print helper
console_print("DuraPy", "cyan", "Welcome to the examples!")

# Progress bar
with Console() as c:
    import time

    task = c.progress.add_task("Processing...", total=100)
    for i in range(0, 101, 20):
        c.progress.update(task, completed=i)
        time.sleep(0.01)
    print("Done!")
