# Songs Directory

Place your audio files and LRC lyrics files in this directory.

## File Structure

```
songs/
├── your_song.mp3
├── your_song.lrc
├── another_song.wav
└── another_song.lrc
```

## Supported Formats

- **Audio**: MP3, WAV
- **Lyrics**: LRC (with timestamps)

## Usage

```bash
# Play a song from this directory
python verse.py songs/your_song.mp3 songs/your_song.lrc
```

## Sample Files

Sample files are included for testing:

- `sample.wav` - Sample audio file
- `sample.lrc` - Sample lyrics file

Test with:

```bash
python verse.py songs/sample.wav songs/sample.lrc
```
