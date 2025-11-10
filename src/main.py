"""
Verse - Terminal Music Player with Synchronized Lyrics
Main orchestrator module for the Verse music player application.
"""

import sys
import time
import os
from dataclasses import dataclass
from typing import Optional
from pathlib import Path


@dataclass
class PlaybackState:
    """Application state management for playback control."""
    current_position: float = 0.0
    current_lyric: Optional[str] = None
    is_playing: bool = False
    lyrics_loaded: bool = False
    audio_loaded: bool = False


class VersePlayer:
    """Main orchestrator class for the Verse music player."""

    def __init__(self, song_path: str, lyrics_path: str):
        """Initialize the Verse player with song and lyrics file paths."""
        self.song_path = Path(song_path)
        self.lyrics_path = Path(lyrics_path)
        self.state = PlaybackState()

        # Import components here to avoid circular imports
        from src.player import AudioPlayer
        from src.lyrics_parser import LyricsParser
        from src.display import LyricDisplay

        # Initialize components
        self.audio_player = AudioPlayer()
        self.lyrics_parser = LyricsParser()
        self.display = LyricDisplay()

        # Track last displayed lyric to avoid redundant updates
        self.last_displayed_lyric: Optional[str] = None

    def _validate_files(self) -> bool:
        """
        Comprehensive file validation and error handling.

        Returns:
            True if all files are valid, False otherwise
        """
        # Check if song file exists
        if not self.song_path.exists():
            self.display.show_error(f"Song file '{self.song_path}' not found")
            return False

        # Check if lyrics file exists
        if not self.lyrics_path.exists():
            self.display.show_error(
                f"Lyrics file '{self.lyrics_path}' not found")
            return False

        # Check file permissions
        if not os.access(self.song_path, os.R_OK):
            self.display.show_error(
                f"Cannot read song file '{self.song_path}' - permission denied")
            return False

        if not os.access(self.lyrics_path, os.R_OK):
            self.display.show_error(
                f"Cannot read lyrics file '{self.lyrics_path}' - permission denied")
            return False

        # Validate audio file format (support both MP3 and WAV for testing)
        if self.song_path.suffix.lower() not in ['.mp3', '.wav']:
            self.display.show_error(
                f"Unsupported audio format '{self.song_path.suffix}'. Only MP3 and WAV files are supported")
            return False

        # Validate LRC file format
        if self.lyrics_path.suffix.lower() not in ['.lrc']:
            self.display.show_error(
                f"Unsupported lyrics format '{self.lyrics_path.suffix}'. Only LRC files are supported")
            return False

        # Check if files are not empty
        if self.song_path.stat().st_size == 0:
            self.display.show_error(f"Song file '{self.song_path}' is empty")
            return False

        if self.lyrics_path.stat().st_size == 0:
            self.display.show_error(
                f"Lyrics file '{self.lyrics_path}' is empty")
            return False

        return True

    def _load_files(self) -> bool:
        """
        Load audio and lyrics files with error handling.

        Returns:
            True if both files loaded successfully, False otherwise
        """
        try:
            # Load audio file
            if not self.audio_player.load_song(str(self.song_path)):
                self.display.show_error(
                    f"Failed to load audio file '{self.song_path}'. File may be corrupted or in an unsupported format")
                return False
            self.state.audio_loaded = True

            # Load lyrics file
            self.lyrics_parser.parse_lrc_file(str(self.lyrics_path))
            self.state.lyrics_loaded = True

            return True

        except FileNotFoundError as e:
            self.display.show_error(f"File not found: {str(e)}")
            return False
        except PermissionError as e:
            self.display.show_error(f"Permission denied: {str(e)}")
            return False
        except ValueError as e:
            self.display.show_error(f"Invalid file format: {str(e)}")
            return False
        except Exception as e:
            self.display.show_error(
                f"Unexpected error loading files: {str(e)}")
            return False

    def start_playback(self) -> None:
        """Begin synchronized playback of audio and lyrics."""
        # Validate files first
        if not self._validate_files():
            return

        # Load files
        if not self._load_files():
            return

        try:
            # Start audio playback
            self.audio_player.play()
            self.state.is_playing = True

            # Clear display and show initial message
            self.display.clear_display()

            # Start synchronization loop
            self._sync_loop()

        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully
            self.display.clear_display()
            self.display.show_error("Playback interrupted by user")
            self.audio_player.stop()
        except Exception as e:
            self.display.show_error(f"Playback error: {str(e)}")
            self.audio_player.stop()

    def _sync_loop(self) -> None:
        """Main synchronization loop for coordinating audio and lyrics."""
        try:
            while self.audio_player.is_playing():
                # Get current playback position
                current_time = self.audio_player.get_position()
                self.state.current_position = current_time

                # Get current lyric for this timestamp
                current_lyric = self.lyrics_parser.get_current_lyric(
                    current_time)

                # Update display only if lyric has changed
                if current_lyric != self.last_displayed_lyric:
                    if current_lyric:
                        self.display.show_lyric(current_lyric)
                    else:
                        # Clear display if no lyric should be shown
                        self.display.clear_display()

                    self.last_displayed_lyric = current_lyric
                    self.state.current_lyric = current_lyric

                # Sleep for 100ms to achieve smooth synchronization
                # This ensures lyrics appear within ±0.2 seconds as specified
                time.sleep(0.1)

            # Playback finished
            self.state.is_playing = False
            self.display.clear_display()

        except Exception as e:
            self.display.show_error(f"Synchronization error: {str(e)}")
            self.audio_player.stop()
            self.state.is_playing = False


def main():
    """Entry point for the Verse music player application."""
    # Handle command-line arguments first
    if len(sys.argv) != 3:
        print("Verse - Terminal Music Player with Synchronized Lyrics")
        print()
        print("Usage: python verse.py <song.mp3> <lyrics.lrc>")
        print()
        print("Arguments:")
        print("  song.mp3    Path to the MP3/WAV audio file")
        print("  lyrics.lrc  Path to the LRC lyrics file")
        print()
        print("Examples:")
        print("  python verse.py songs/my_song.mp3 songs/my_song.lrc")
        print("  python verse.py songs/sample.wav songs/sample.lrc")
        sys.exit(1)

    # Check dependencies after argument validation
    try:
        import pygame
        import rich
    except ImportError as e:
        print(f"Missing required dependency: {e}")
        print("Please install required packages: pip install pygame rich")
        sys.exit(1)

    song_path = sys.argv[1]
    lyrics_path = sys.argv[2]

    try:
        # Create and start the player
        # File validation is handled within the VersePlayer class
        player = VersePlayer(song_path, lyrics_path)
        player.start_playback()

    except KeyboardInterrupt:
        print("\nPlayback interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
