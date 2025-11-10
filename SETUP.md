# Complete Setup Guide

This guide will walk you through setting up Verse from scratch.

## Prerequisites

- Python 3.7 or higher
- Working audio output on your system
- Terminal with color support

## Step-by-Step Setup

### 1. Verify Python Installation

```bash
python --version
```

You should see Python 3.7 or higher. If not, download Python from [python.org](https://www.python.org/).

### 2. Create Virtual Environment

A virtual environment keeps your project dependencies isolated.

**Windows (PowerShell):**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**

```cmd
python -m venv venv
venv\Scripts\activate.bat
```

**Linux/macOS:**

```bash
python -m venv venv
source venv/bin/activate
```

**Quick Activation (Windows):**
We've included helper scripts:

- PowerShell: `.\activate.ps1`
- CMD: `activate.bat`

### 3. Install Dependencies

With your virtual environment activated:

```bash
pip install -r requirements.txt
```

This will install:

- `pygame` - Audio playback engine
- `rich` - Terminal formatting and colors

### 4. Verify Installation

```bash
python -c "import pygame, rich; print('✓ All dependencies installed!')"
```

### 5. Test with Sample Files

```bash
python verse.py songs/sample.wav songs/sample.lrc
```

You should see:

- Audio playing through your speakers
- Lyrics appearing in the terminal, centered and colored
- Lyrics changing in sync with the audio

Press `Ctrl+C` to stop playback.

## Adding Your Own Songs

### Option 1: Use Existing LRC Files

1. Find or download LRC files for your songs (search "[song name] lrc file")
2. Place both the audio file and LRC file in the `songs/` directory
3. Run:
   ```bash
   python verse.py songs/your_song.mp3 songs/your_song.lrc
   ```

### Option 2: Create Your Own LRC Files

1. Create a new text file: `songs/your_song.lrc`
2. Add timestamps and lyrics:
   ```lrc
   [00:00.00]First line of lyrics
   [00:05.50]Second line of lyrics
   [00:10.00]Third line of lyrics
   ```
3. Run:
   ```bash
   python verse.py songs/your_song.mp3 songs/your_song.lrc
   ```

## Troubleshooting

### Virtual Environment Not Activating

**Windows PowerShell - Execution Policy Error:**

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Alternative - Use Command Prompt:**

```cmd
venv\Scripts\activate.bat
```

### Dependencies Won't Install

**Upgrade pip first:**

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

**pygame Installation Fails (Windows):**

- Install Visual C++ Build Tools from Microsoft
- Or try: `pip install pygame --pre`

**pygame Installation Fails (Linux):**

```bash
# Ubuntu/Debian
sudo apt-get install python3-dev libasound2-dev

# Then retry
pip install -r requirements.txt
```

### No Audio Output

1. Check system volume and audio settings
2. Test audio with another application
3. Ensure pygame can access audio:
   ```bash
   python -c "import pygame; pygame.mixer.init(); print('Audio OK')"
   ```

### File Not Found Errors

- Ensure files are in the `songs/` directory
- Check file names match exactly (case-sensitive on Linux/macOS)
- Use full paths if needed:
  ```bash
  python verse.py C:\Music\song.mp3 C:\Music\song.lrc
  ```

## Daily Usage

### Starting a Session

1. **Activate virtual environment:**

   ```bash
   # Windows PowerShell
   .\activate.ps1

   # Windows CMD
   activate.bat

   # Linux/macOS
   source venv/bin/activate
   ```

2. **Run Verse:**

   ```bash
   python verse.py songs/your_song.mp3 songs/your_song.lrc
   ```

3. **Deactivate when done:**
   ```bash
   deactivate
   ```

## Next Steps

- Read [QUICKSTART.md](QUICKSTART.md) for quick reference
- See [README.md](README.md) for complete documentation
- Check [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for project organization

## Getting Help

If you encounter issues:

1. Check the [Troubleshooting section in README.md](README.md#troubleshooting)
2. Verify all prerequisites are met
3. Ensure virtual environment is activated
4. Test with sample files first

Enjoy your music with synchronized lyrics! 🎵
