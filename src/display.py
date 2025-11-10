"""
Display Module for Verse Music Player
Handles terminal rendering and lyric display using rich library.
"""

from rich.console import Console
from rich.text import Text
from rich.align import Align
from typing import Optional


class LyricDisplay:
    """Terminal display component for rendering synchronized lyrics."""

    def __init__(self, console: Optional[Console] = None):
        """
        Initialize the lyric display.

        Args:
            console: Rich console instance, creates new one if None
        """
        # Configure rich console settings for optimal terminal rendering
        if console is None:
            self.console = Console(
                force_terminal=True,
                color_system="auto",
                width=None,  # Auto-detect terminal width
                height=None,  # Auto-detect terminal height
                legacy_windows=False,
                stderr=False,  # Use stdout for consistent output
                highlight=False  # Disable syntax highlighting for plain text
            )
        else:
            self.console = console
        self.last_displayed: Optional[str] = None

    def show_lyric(self, text: str) -> None:
        """
        Display a lyric line with formatting and centering.

        Args:
            text: The lyric text to display
        """
        if not text or text == self.last_displayed:
            return

        # Clear the display first to prevent flickering
        self.clear_display()

        # Create styled text with consistent color formatting
        styled_text = Text(text, style="bold cyan")

        # Center the text in the terminal
        centered_text = Align.center(styled_text)

        # Print the centered, styled text with consistent formatting
        self.console.print(centered_text, end="\n")

        # Update last displayed text
        self.last_displayed = text

    def clear_display(self) -> None:
        """Clear the terminal display to prevent flickering."""
        self.console.clear()

    def show_error(self, message: str) -> None:
        """
        Display an error message to the user.

        Args:
            message: Error message to display
        """
        # Clear display first for consistent presentation
        self.clear_display()

        # Create styled error text with red color
        error_text = Text(f"Error: {message}", style="bold red")

        # Center the error message
        centered_error = Align.center(error_text)

        # Print the error message
        self.console.print(centered_error)

        # Reset last displayed to ensure next lyric shows properly
        self.last_displayed = None
