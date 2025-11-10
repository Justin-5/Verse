"""
Audio Player Module for Verse Music Player
Handles MP3 playback using pygame.mixer.
"""

from typing import Optional
import pygame
import os
from pathlib import Path


class AudioPlayer:
    """Audio player component using pygame.mixer for MP3 playback."""

    def __init__(self):
        """Initialize the audio player."""
        self.loaded_file: Optional[str] = None
        self._is_playing: bool = False
        self._start_time: float = 0.0
        self._pause_time: float = 0.0
        self._mixer_initialized: bool = False

        # Initialize pygame mixer
        try:
            pygame.mixer.pre_init(frequency=22050, size=-
                                  16, channels=2, buffer=512)
            pygame.mixer.init()
            self._mixer_initialized = True
        except pygame.error as e:
            raise RuntimeError(f"Failed to initialize pygame mixer: {e}")

    def load_song(self, file_path: str) -> bool:
        """
        Load an MP3 file for playback.

        Args:
            file_path: Path to the MP3 file

        Returns:
            True if file loaded successfully, False otherwise
        """
        if not self._mixer_initialized:
            return False

        # Validate file existence
        if not os.path.exists(file_path):
            return False

        # Validate file extension (support both MP3 and WAV for testing)
        path = Path(file_path)
        if path.suffix.lower() not in ['.mp3', '.wav']:
            return False

        # Validate file is readable
        if not os.access(file_path, os.R_OK):
            return False

        try:
            # Stop any currently playing music
            if self._is_playing:
                self.stop()

            # Load the music file
            pygame.mixer.music.load(file_path)
            self.loaded_file = file_path
            return True

        except pygame.error:
            self.loaded_file = None
            return False

    def play(self) -> None:
        """Start audio playback."""
        if not self._mixer_initialized or not self.loaded_file:
            return

        try:
            if not self._is_playing:
                pygame.mixer.music.play()
                self._start_time = pygame.time.get_ticks() / 1000.0
                self._is_playing = True
                # Small delay to ensure pygame recognizes playback has started
                import time
                time.sleep(0.1)
        except pygame.error:
            self._is_playing = False

    def stop(self) -> None:
        """Stop audio playback."""
        if not self._mixer_initialized:
            return

        try:
            pygame.mixer.music.stop()
            self._is_playing = False
            self._start_time = 0.0
            self._pause_time = 0.0
        except pygame.error:
            pass

    def get_position(self) -> float:
        """
        Get current playback position in seconds.

        Returns:
            Current playback time in seconds
        """
        if not self._mixer_initialized or not self._is_playing:
            return 0.0

        try:
            # pygame.mixer.music.get_pos() returns milliseconds since music started
            pos_ms = pygame.mixer.music.get_pos()
            if pos_ms < 0:
                # get_pos() returns -1 if music hasn't started yet
                return 0.0
            return pos_ms / 1000.0
        except pygame.error:
            return 0.0

    def is_playing(self) -> bool:
        """
        Check if audio is currently playing.

        Returns:
            True if audio is playing, False otherwise
        """
        if not self._mixer_initialized:
            return False

        try:
            # Check if pygame mixer is busy (playing music)
            is_busy = pygame.mixer.music.get_busy()

            # Update internal state if music stopped
            if not is_busy and self._is_playing:
                self._is_playing = False

            return is_busy and self._is_playing
        except pygame.error:
            return False
