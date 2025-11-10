# Quick Start Guide

Get started with Verse in 3 simple steps!

## 1. Set Up Virtual Environment (Recommended)

### Windows (PowerShell)

```powershell
# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Or use the activation script
.\activate.ps1
```

### Windows (Command Prompt)

```cmd
# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate.bat

# Or use the activation script
activate.bat
```

### Linux/macOS

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate
```

## 2. Install Dependencies

```bash
# Install from requirements.txt
pip install -r requirements.txt

# Or install manually
pip install pygame rich
```

## 3. Test with Sample Files

```bash
python verse.py songs/sample.wav songs/sample.lrc
```

## 4. Add Your Own Songs

1. Place your audio file (MP3 or WAV) in the `songs/` directory
2. Place your LRC lyrics file in the `songs/` directory
3. Run:

```bash
python verse.py songs/your_song.mp3 songs/your_song.lrc
```

## Need LRC Files?

### Option 1: Find Online

Search for "[song name] lrc file" and download

### Option 2: Create Your Own

1. Create a text file: `your_song.lrc`
2. Add timestamps and lyrics:

```lrc
[00:00.00]First line of lyrics
[00:05.50]Second line of lyrics
[00:10.00]Third line of lyrics
```

## Controls

- **Ctrl+C** to stop playback

## Troubleshooting

**Dependencies not installed?**

```bash
pip install pygame rich
```

**File not found?**

- Make sure files are in the `songs/` directory
- Check file names match exactly

**Need help?**
See the full [README.md](README.md) for detailed documentation.
