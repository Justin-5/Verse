"""
Display Module for Verse Music Player
Handles terminal rendering and lyric display using rich library.
"""

from rich.console import Console
from rich.text import Text
from rich.align import Align
from rich.panel import Panel
from typing import Optional, List, Tuple


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
        self.song_duration: float = 0.0  # Total song duration in seconds

    def _format_time(self, seconds: float) -> str:
        """
        Format time in seconds to MM:SS format.

        Args:
            seconds: Time in seconds

        Returns:
            Formatted time string
        """
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes:02d}:{secs:02d}"

    def _create_progress_bar(self, current: float, total: float, width: int = 20) -> Text:
        """
        Create a compact visual progress bar with time display for left side.

        Args:
            current: Current playback position in seconds
            total: Total duration in seconds
            width: Width of the progress bar in characters

        Returns:
            Rich Text object with the progress bar
        """
        if total <= 0:
            percentage = 0
        else:
            percentage = min(100, (current / total) * 100)

        filled_width = int((percentage / 100) * width)
        empty_width = width - filled_width

        # Create compact progress bar
        progress_text = Text()
        progress_text.append(self._format_time(current), style="bold cyan")
        progress_text.append(" ", style="dim white")

        # Progress bar with filled portion in magenta and empty in gray
        # Using different characters that render better in terminals
        progress_text.append("▓" * filled_width, style="bold magenta")
        progress_text.append("░" * empty_width, style="dim white")
        progress_text.append(" ", style="dim white")

        return progress_text

    def show_lyric_with_context(
        self,
        current_text: str,
        previous_text: Optional[str] = None,
        next_text: Optional[str] = None,
        current_time: float = 0.0,
        clear_screen: bool = False
    ) -> None:
        """
        Display current lyric with context (previous and next lines) and progress bar on the left.
        Words appear one at a time on the same line (karaoke style).

        Args:
            current_text: The current lyric text to display
            previous_text: The previous lyric line (dimmed)
            next_text: The next lyric line (dimmed)
            current_time: Current playback position in seconds
            clear_screen: If True, clear the entire screen and redraw everything (new line)
        """
        if not current_text:
            return

        # If starting a new line, clear screen and draw context
        if clear_screen:
            self.console.clear()

            # Print some spacing at top
            self.console.print()

            # Print previous lyric (dimmed) - no progress bar
            if previous_text:
                prev_text = Text()
                # Spacing for alignment
                prev_text.append("                           ")
                prev_text.append(previous_text, style="dim white")
                self.console.print(Align.center(prev_text))
                self.console.print()
            else:
                self.console.print()

            # Print placeholder for current line (will be updated)
            self.console.print()

            # Print next lyric (dimmed) - no progress bar
            if next_text:
                next_styled = Text()
                # Spacing for alignment
                next_styled.append("                           ")
                next_styled.append(next_text, style="dim white")
                self.console.print(Align.center(next_styled))
            else:
                self.console.print()

            # Move cursor back up to the current line position
            # We need to go up: 1 (next lyric or empty) + 1 (current line)
            self.console.file.write("\033[2F")
            self.console.file.flush()

        # If not a new line, just move cursor up to overwrite current line
        elif self.last_displayed:
            # Move cursor up one line and clear it
            self.console.file.write("\033[F\033[K")
            self.console.file.flush()

        # Get progress bar for left side (fixed position)
        progress_bar = self._create_progress_bar(
            current_time, self.song_duration)

        # Create styled current lyric with fading gradient (centered)
        current_styled = Text()
        words = current_text.split()

        # Create fading gradient: newest word is brightest, older words fade
        # Using cyan as the base color with fading intensity
        num_words = len(words)
        for i, word in enumerate(words):
            # Calculate fade level - most recent word (last) is brightest
            # Earlier words get progressively dimmer
            if num_words <= 1:
                # Single word - make it bright
                color = "bold cyan"
            elif i == num_words - 1:
                # Last word (most recent) - brightest
                color = "bold cyan"
            elif i == num_words - 2:
                # Second to last - bright but not bold
                color = "cyan"
            elif i == num_words - 3:
                # Third to last - dimmer
                color = "bright_cyan"
            else:
                # Older words - dimmest
                color = "dim cyan"

            current_styled.append(word, style=color)
            if i < len(words) - 1:
                current_styled.append(" ")

        # Create the full line with progress bar on left and centered lyrics
        # Progress bar: time (5 chars) + space (1) + bar (20) + space (1) = ~27 chars
        progress_bar_width = 27

        # Get terminal width
        terminal_width = self.console.width or 120

        # Calculate how much space we have for centering the lyrics
        available_width = terminal_width - progress_bar_width
        lyric_length = len(current_text)

        # Calculate padding to center lyrics in available space
        left_padding = max(0, (available_width - lyric_length) // 2)

        # Build the complete line
        full_line = Text()
        full_line.append_text(progress_bar)
        full_line.append(" " * left_padding)
        full_line.append_text(current_styled)

        # Print the complete line
        self.console.print(full_line)

        # Update last displayed text
        self.last_displayed = current_text

    def show_lyric(self, text: str, clear_line: bool = False) -> None:
        """
        Display a lyric line with formatting and centering.
        (Legacy method - kept for backward compatibility)

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

        # Create styled text with gradient color formatting
        styled_text = Text()
        words = text.split()

        # Apply gradient colors across words
        colors = ["bold cyan", "bold blue",
                  "bold magenta", "bold blue", "bold cyan"]
        for i, word in enumerate(words):
            color = colors[i % len(colors)]
            styled_text.append(word, style=color)
            if i < len(words) - 1:
                styled_text.append(" ")

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

    def set_song_duration(self, duration: float) -> None:
        """
        Set the total song duration for progress bar display.

        Args:
            duration: Total song duration in seconds
        """
        self.song_duration = duration

    def show_song_header(self, song_name: str, duration: float = 0.0) -> None:
        """
        Display the song name as a header at the top of the screen.

        Args:
            song_name: Name of the song being played
            duration: Total song duration in seconds
        """
        self.clear_display()
        self.song_duration = duration

        # Calculate the width based on song name length
        song_text = f"♪  {song_name}  ♪"
        text_width = len(song_text)

        # Make decorative line match the text width
        header_line = "═" * text_width

        # Create styled header text with single color
        header_text = Text()
        header_text.append("\n")
        header_text.append(header_line, style="bold cyan")
        header_text.append("\n")

        # Apply single color to song name
        header_text.append("♪  ", style="bold cyan")
        header_text.append(song_name, style="bold cyan")
        header_text.append("  ♪", style="bold cyan")

        header_text.append("\n")
        header_text.append(header_line, style="bold cyan")

        # Add duration if available
        if duration > 0:
            duration_text = f"\nDuration: {self._format_time(duration)}"
            header_text.append(duration_text, style="dim cyan")

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
