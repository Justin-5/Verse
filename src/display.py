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

    def show_lyric(self, text: str, clear_line: bool = False) -> None:
        """
        Display a lyric line with formatting and centering.

        Args:
            text: The lyric text to display
            clear_line: If True, clear the current line before displaying
        """
        if not text or text == self.last_displayed:
            return

        # If clear_line is True, clear the entire display (for new lines)
        if clear_line:
            self.console.clear()
            # Print newline to position cursor
            self.console.print()

        # Create styled text with consistent color formatting
        styled_text = Text(text, style="bold cyan")

        # Center the text in the terminal
        centered_text = Align.center(styled_text)

        # Move cursor up one line and clear it, then print
        # This overwrites the previous line instead of creating a new one
        if not clear_line and self.last_displayed:
            # Move cursor up and clear the line
            self.console.file.write("\033[F\033[K")
            self.console.file.flush()

        # Print the centered text
        self.console.print(centered_text)

        # Update last displayed text
        self.last_displayed = text

    def clear_display(self) -> None:
        """Clear the terminal display to prevent flickering."""
        self.console.clear()

    def show_song_header(self, song_name: str) -> None:
        """
        Display the song name as a header at the top of the screen.

        Args:
            song_name: Name of the song being played
        """
        self.clear_display()

        # Calculate the width based on song name length
        song_text = f"♪  {song_name}  ♪"
        text_width = len(song_text)

        # Make decorative line match the text width
        header_line = "═" * text_width

        # Create styled header text
        header_text = Text()
        header_text.append("\n")
        header_text.append(header_line, style="bold magenta")
        header_text.append("\n")
        header_text.append(song_text, style="bold yellow")
        header_text.append("\n")
        header_text.append(header_line, style="bold magenta")
        header_text.append("\n\n")

        # Center the header
        centered_header = Align.center(header_text)

        # Print the header
        self.console.print(centered_header)

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
