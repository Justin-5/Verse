"""
Lyrics Parser Module for Verse Music Player
Handles parsing of LRC format lyric files and timestamp management.
"""

from dataclasses import dataclass
from typing import List, Optional
import re


@dataclass
class LyricLine:
    """Data structure for storing timestamped lyric lines."""
    timestamp: float  # Time in seconds
    text: str        # Lyric text

    def __post_init__(self):
        """Validate the lyric line data after initialization."""
        if self.timestamp < 0:
            raise ValueError("Timestamp cannot be negative")
        if not isinstance(self.text, str):
            raise ValueError("Text must be a string")


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
