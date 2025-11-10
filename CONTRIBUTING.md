# Contributing to Verse

Thank you for your interest in contributing to Verse!

## What Gets Committed

The following files are tracked in git:

### Source Code

- `src/` - All Python source files
- `verse.py` - Main entry point

### Documentation

- `README.md` - Main documentation
- `QUICKSTART.md` - Quick start guide
- `SETUP.md` - Detailed setup instructions
- `PROJECT_STRUCTURE.md` - Project organization
- `CONTRIBUTING.md` - This file

### Configuration

- `requirements.txt` - Python dependencies
- `.gitignore` - Git ignore rules
- `activate.ps1` / `activate.bat` - Virtual environment helpers

### Sample Files

- `songs/sample.wav` - Sample audio for testing
- `songs/sample.lrc` - Sample lyrics for testing
- `songs/README.md` - Songs directory guide

### Specifications

- `.kiro/specs/` - Feature specifications and design docs

## What's Ignored

The following are NOT committed (see `.gitignore`):

### Generated Files

- `__pycache__/` - Python bytecode
- `*.pyc`, `*.pyo` - Compiled Python files
- `.pytest_cache/` - Test cache

### Virtual Environment

- `venv/` - Virtual environment directory
- `env/`, `ENV/` - Alternative venv names

### User Content

- `songs/*.mp3` - User's music files
- `songs/*.wav` - User's audio files (except sample)
- `songs/*.lrc` - User's lyrics files (except sample)

### IDE Files

- `.vscode/` - VS Code settings
- `.idea/` - PyCharm settings
- `.kiro/` - Kiro IDE specifications
- `*.swp`, `*.swo` - Vim swap files

### OS Files

- `.DS_Store` - macOS metadata
- `Thumbs.db` - Windows thumbnails

### Debug/Test Files

- `debug*.py` - Debug scripts
- `test_*.py` - Test scripts
- `*.log` - Log files

## Development Workflow

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/verse.git
cd verse
```

### 2. Set Up Development Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
.\venv\Scripts\Activate.ps1  # Windows PowerShell
# or
source venv/bin/activate      # Linux/macOS

# Install dependencies
pip install -r requirements.txt
```

### 3. Make Changes

- Edit source files in `src/`
- Test your changes with sample files
- Update documentation if needed

### 4. Test Your Changes

```bash
# Test with sample files
python verse.py songs/sample.wav songs/sample.lrc

# Add your own test files to songs/ (they won't be committed)
python verse.py songs/test.mp3 songs/test.lrc
```

### 5. Commit Your Changes

```bash
# Check what will be committed
git status

# Add your changes
git add src/
git add README.md  # if you updated docs

# Commit with a clear message
git commit -m "Add feature: description of your changes"
```

### 6. Push to GitHub

```bash
git push origin main
```

## Code Style

- Follow PEP 8 conventions
- Use type hints for function parameters and returns
- Add docstrings to all classes and methods
- Keep functions focused and under 50 lines when possible
- Comment complex logic

## Adding Features

1. Create a spec in `.kiro/specs/` if it's a major feature
2. Update documentation in `README.md`
3. Add tests if applicable
4. Ensure backward compatibility

## Questions?

Feel free to open an issue on GitHub for:

- Bug reports
- Feature requests
- Questions about the code
- Documentation improvements

Happy coding! 🎵
