"""DuraPy UniCLI Exceptions Module"""

from ..shared.color_system import color_text


class UnknownModule(Exception):
    """UniCLI Unknown Command Module"""

    def __init__(self, given_module: str):
        super().__init__(f"Unknown Module: {color_text(given_module, 'red')}")


class UnknownSubCommand(Exception):
    """Raises when an unknown subcommand gets caught in validate_command()."""

    def __init__(self, module: str, given_command: str):
        super().__init__(
            f"Unknown command for {module}: {color_text(given_command, 'red')}"
        )


class MissingSubCommand(Exception):
    """Raises when the subcommand is missing from a command string."""

    def __init__(self, module):
        super().__init__(f"Missing subcommand for {module}")


class EmptyTokenList(Exception):
    """Raises when the TokenList passed into validate_command() is empty."""

    def __init__(self):
        super().__init__(
            "Empty TokenList! Make sure of correct tokens before verification attempt."
        )
