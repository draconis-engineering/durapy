"""DuraPy UniCLI Source"""

import os
import subprocess

from rich.progress import Progress, SpinnerColumn, TextColumn

from ..shared.color_system import color_text


def clear_terminal() -> None:
    """Clear the terminal screen."""
    subprocess.run(["cls" if os.name == "nt" else "clear"], shell=True, check=False)


def console_msg(
    sender: str, sender_color: str, info: str, info_color: str = "white"
) -> str:
    return f"[{color_text(sender, sender_color)}] >>> {color_text(info, info_color)}"


def console_print(
    sender: str, sender_color: str, info: str, info_color: str = "white"
) -> None:
    print(console_msg(sender, sender_color, info, info_color))


def console_input(
    sender: str, sender_color: str, prompt: str = "", prompt_color: str = "white"
) -> str | float:
    user_input = input(console_msg(sender, sender_color, prompt, prompt_color) + " ")
    try:
        return float(user_input)
    except ValueError:
        return user_input


def console_confirm(
    sender: str, sender_color: str, prompt_info: str, prompt_color: str = "white"
) -> bool:
    while True:
        user_input = (
            input(
                console_msg(sender, sender_color, prompt_info + ":", prompt_color) + " "
            )
            .lower()
            .strip()
        )
        if user_input in ["y", "ye", "yes"]:
            return True
        elif user_input in ["n", "no"]:
            return False
        else:
            print(
                f"Please enter {color_text('y', 'green')} or {color_text('n', 'red')}"
            )


class Console:
    def __init__(self):
        self.progress = Progress(
            SpinnerColumn(spinner_name="dots"),
            TextColumn("{task.description}"),
            transient=False,  # Keeps completed tasks visible on screen
        )
        # Dictionary mapping: { "task_name": task_id }
        self.active_tasks = {}

    def __enter__(self):
        self.progress.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.progress.stop()

    def start_task(self, name: str):
        """Kicks off a task. Names must be unique if running concurrently."""
        if name in self.active_tasks:
            raise ValueError(f"Task '{name}' is already running.")

        task_id = self.progress.add_task(
            description=f"Starting task: {name} ...", total=None
        )
        self.active_tasks[name] = task_id

    def end_task(self, name: str, success: bool = True, error_msg: str | None = None):
        """Resolves any specific task by its unique name, regardless of order."""
        task_id = self.active_tasks.pop(name, None)

        if task_id is None:
            raise KeyError(f"No active task found with the name '{name}'.")

        if success:
            status_text = (
                f"Starting task: {name} ... [bold green]Finished![/bold green]"
            )
        else:
            status_text = f"Starting task: {name} ... [bold red]Failed![/bold red]" + (
                f" Error: {error_msg}" if error_msg else ""
            )

        self.progress.update(task_id, description=status_text, completed=True)

    def print(self, text, style):
        """Prints a message to the console with a specific style."""
        self.progress.console.print(text, style=style)
