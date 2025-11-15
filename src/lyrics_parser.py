"""
Lyrics Parser Module for Verse Music Player
Handles parsing of LRC format lyric files and timestamp management.
"""

from dataclasses import dataclass
from typing import List, Optional
import re


@dataclass
class LyricWord:
    """Data structure for storing individual word with timestamp."""
    timestamp: float  # Time in seconds when word should appear
    text: str        # Word text
    line_index: int  # Which line this word belongs to


@dataclass
class LyricLine:
    """Data structure for storing timestamped lyric lines."""
    timestamp: float  # Time in seconds
    text: str        # Lyric text
    words: List['LyricWord'] = None  # Optional word-level timing

    def __post_init__(self):
        """Validate the lyric line data after initialization."""
        if self.timestamp < 0:
            raise ValueError("Timestamp cannot be negative")
        if not isinstance(self.text, str):
            raise ValueError("Text must be a string")
        if self.words is None:
            self.words = []


class LyricsParser:
    """Parser for LRC format lyric files."""

    def __init__(self):
        """Initialize the lyrics parser."""
        self.lyrics: List[LyricLine] = []

    def parse_lrc_file(self, file_path: str) -> List[LyricLine]:
        """
        Parse an LRC file and extract timestamp-lyric pairs.

        Args:
            file_path: Path to the LRC file

        Returns:
            List of LyricLine objects sorted by timestamp
        """
        lyrics = []

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                for line_number, line in enumerate(file, 1):
                    line = line.strip()
                    if not line:
                        continue

                    # Match LRC format: [mm:ss.xx]lyric text or [mm:ss]lyric text
                    match = re.match(
                        r'\[(\d{1,2}):(\d{2})(?:\.(\d{2}))?\](.*)', line)
                    if match:
                        try:
                            minutes = int(match.group(1))
                            seconds = int(match.group(2))
                            centiseconds = int(match.group(
                                3)) if match.group(3) else 0
                            text = match.group(4).strip()

                            # Validate timestamp components
                            if seconds >= 60 or centiseconds >= 100:
                                print(
                                    f"Warning: Invalid timestamp on line {line_number}: {line}")
                                continue

                            # Convert to total seconds
                            timestamp = minutes * 60 + seconds + centiseconds / 100.0

                            # Skip empty lyrics but allow them for timing purposes
                            lyrics.append(
                                LyricLine(timestamp=timestamp, text=text))

                        except (ValueError, TypeError) as e:
                            print(
                                f"Warning: Invalid timestamp on line {line_number}: {line}")
                            continue
                    else:
                        # Skip non-lyric lines (metadata, etc.)
                        continue

            # Sort by timestamp for efficient lookup
            lyrics.sort(key=lambda x: x.timestamp)

            # Generate word-level timing automatically
            self._generate_word_timing(lyrics)

            self.lyrics = lyrics
            return lyrics

        except FileNotFoundError:
            raise FileNotFoundError(f"LRC file not found: {file_path}")
        except PermissionError:
            raise PermissionError(
                f"Permission denied reading LRC file: {file_path}")
        except UnicodeDecodeError:
            raise ValueError(
                f"Invalid file encoding. LRC file must be UTF-8: {file_path}")
        except Exception as e:
            raise ValueError(f"Error parsing LRC file {file_path}: {str(e)}")

    def get_current_lyric(self, timestamp: float) -> Optional[str]:
        """
        Get the current lyric line for a given timestamp.

        Args:
            timestamp: Current playback time in seconds

        Returns:
            The lyric text that should be displayed at the given timestamp
        """
        if not self.lyrics:
            return None

        # Find the most recent lyric line that should be displayed
        current_lyric = None
        for lyric_line in self.lyrics:
            if lyric_line.timestamp <= timestamp:
                current_lyric = lyric_line.text
            else:
                # Since lyrics are sorted, we can break early
                break

        return current_lyric

    def get_current_words(self, timestamp: float) -> Optional[str]:
        """
        Get the current words that should be displayed up to the given timestamp.
        This enables word-by-word karaoke-style display.

        Args:
            timestamp: Current playback time in seconds

        Returns:
            String of words that should be displayed so far
        """
        if not self.lyrics:
            return None

        # Find which line we're currently in
        current_line_index = -1
        for i, lyric_line in enumerate(self.lyrics):
            if lyric_line.timestamp <= timestamp:
                current_line_index = i
            else:
                break

        if current_line_index < 0:
            return None

        current_line = self.lyrics[current_line_index]

        # If no word-level timing, return full line
        if not current_line.words:
            return current_line.text

        # Build string of words that should be visible
        visible_words = []
        for word in current_line.words:
            if word.timestamp <= timestamp:
                visible_words.append(word.text)
            else:
                break

        return ' '.join(visible_words) if visible_words else None

        # Find which line we're currently in
        current_line_index = -1
        for i, lyric_line in enumerate(self.lyrics):
            if lyric_line.timestamp <= timestamp:
                current_line_index = i
            else:
                break

        if current_line_index < 0:
            return None

        current_line = self.lyrics[current_line_index]

        # If no word-level timing, return full line
        if not current_line.words:
            return current_line.text

        # Build string of words that should be visible
        visible_words = []
        for word in current_line.words:
            if word.timestamp <= timestamp:
                visible_words.append(word.text)
            else:
                break

        return ' '.join(visible_words) if visible_words else None

    def _generate_word_timing(self, lyrics: List[LyricLine]) -> None:
        """
        Automatically generate word-level timing for each line.
        Distributes words evenly across the duration until the next line.

        Args:
            lyrics: List of lyric lines to process
        """
        for i, line in enumerate(lyrics):
            if not line.text:
                continue

            # Split line into words
            words = line.text.split()
            if not words:
                continue

            # Calculate duration until next line (or default 4 seconds)
            if i < len(lyrics) - 1:
                duration = lyrics[i + 1].timestamp - line.timestamp
            else:
                duration = 4.0  # Default duration for last line

            # Distribute words evenly across the duration
            time_per_word = duration / len(words)

            line.words = []
            for word_index, word in enumerate(words):
                word_timestamp = line.timestamp + (word_index * time_per_word)
                line.words.append(LyricWord(
                    timestamp=word_timestamp,
                    text=word,
                    line_index=i
                ))

    def get_current_word_only(self, timestamp: float) -> Optional[str]:
        """
        Get only the current word being sung (not accumulated).
        Shows one word at a time without previous words.

        Args:
            timestamp: Current playback time in seconds

        Returns:
            Only the current word that should be displayed
        """
        if not self.lyrics:
            return None

        # Find which line we're currently in
        current_line_index = -1
        for i, lyric_line in enumerate(self.lyrics):
            if lyric_line.timestamp <= timestamp:
                current_line_index = i
            else:
                break

        if current_line_index < 0:
            return None

        current_line = self.lyrics[current_line_index]

        # If no word-level timing, return full line
        if not current_line.words:
            return current_line.text

        # Find the current word only (not accumulated)
        current_word = None
        for word in current_line.words:
            if word.timestamp <= timestamp:
                current_word = word.text
            else:
                break

        return current_word

    def get_current_line_index(self, timestamp: float) -> int:
        """
        Get the index of the current line being displayed.
        Used to detect when we move to a new line.

        Args:
            timestamp: Current playback time in seconds

        Returns:
            Index of current line, or -1 if no line is active
        """
        if not self.lyrics:
            return -1

        current_line_index = -1
        for i, lyric_line in enumerate(self.lyrics):
            if lyric_line.timestamp <= timestamp:
                current_line_index = i
            else:
                break

        return current_line_index
