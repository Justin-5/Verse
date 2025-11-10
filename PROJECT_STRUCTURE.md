# Project Structure

## Optimized Folder Organization

```
verse/
├── src/                    # Source code (modular architecture)
│   ├── __init__.py         # Package initialization
│   ├── main.py             # Main orchestrator and entry point
│   ├── player.py           # Audio playback engine (pygame)
│   ├── lyrics_parser.py    # LRC file parser
│   └── display.py          # Terminal display (rich)
│
├── songs/                  # Songs and lyrics storage
│   ├── README.md           # Guide for adding songs
│   ├── sample.wav          # Sample audio file
│   └── sample.lrc          # Sample lyrics file
│
├── venv/                   # Virtual environment (created by user)
│
├── .kiro/                  # Kiro IDE specifications
│   └── specs/              # Feature specifications
│
├── verse.py                # Main entry point
├── requirements.txt        # Python dependencies
├── activate.ps1            # PowerShell activation script
├── activate.bat            # CMD activation script
├── .gitignore              # Git ignore rules
├── QUICKSTART.md           # Quick start guide
├── PROJECT_STRUCTURE.md    # This file
└── README.md               # Complete documentation
```

## Key Improvements

### 1. Organized Source Code

- All Python modules moved to `src/` directory
- Clean separation of concerns
- Proper package structure with `__init__.py`

### 2. Dedicated Songs Directory

- `songs/` folder for all audio and lyrics files
- Includes sample files for testing
- README guide for adding new songs
- Gitignore configured to exclude user songs (keeps samples)

### 3. Simplified Entry Point

- Single `verse.py` file as main entry point
- Clear, memorable command: `python verse.py`
- Updated all documentation to reflect new structure

### 4. Removed Unnecessary Files

**Deleted:**

- Old root-level module files (main.py, player.py, etc.)
- Test files (test_player.py, test_lyrics_parser.py)
- Utility scripts (create_sample_audio.py, run_sample.py)
- Duplicate audio files (sample_song.wav, song.wav, etc.)
- Duplicate lyrics files (sample_lyrics.lrc, lyrics.lrc)

### 5. Added Essential Files

**New:**

- `requirements.txt` - Easy dependency installation
- `QUICKSTART.md` - Quick start guide for new users
- `PROJECT_STRUCTURE.md` - This documentation
- `.gitignore` - Proper git configuration
- `songs/README.md` - Guide for songs directory

## Usage

### Setting Up Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows PowerShell)
.\venv\Scripts\Activate.ps1
# Or use: .\activate.ps1

# Activate (Windows CMD)
venv\Scripts\activate.bat
# Or use: activate.bat

# Activate (Linux/macOS)
source venv/bin/activate
```

### Installing Dependencies

```bash
pip install -r requirements.txt
```

### Running the Application

```bash
# Test with samples
python verse.py songs/sample.wav songs/sample.lrc

# Use your own songs
python verse.py songs/your_song.mp3 songs/your_song.lrc
```

### Adding New Songs

1. Place audio file in `songs/` directory
2. Place LRC file in `songs/` directory
3. Run with the file paths

### Installing Dependencies

```bash
pip install -r requirements.txt
```

## Benefits

1. **Cleaner Root Directory** - Only essential files at root level
2. **Better Organization** - Source code separated from data
3. **Easier Navigation** - Clear folder structure
4. **Git-Friendly** - Proper gitignore for user content
5. **Professional Structure** - Follows Python best practices
6. **User-Friendly** - Dedicated songs folder for easy file management
7. **Maintainable** - Modular architecture in src/ directory

## Migration Notes

If you had the old structure:

- Old: `python main.py song.wav lyrics.lrc`
- New: `python verse.py songs/song.wav songs/lyrics.lrc`

All functionality remains the same, just better organized!
