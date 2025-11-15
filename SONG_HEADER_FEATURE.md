# Song Header Feature

## Overview

Before lyrics start displaying, Verse shows a beautiful centered header with the song name.

## Visual Example

```
════════════════════════════════════════════════════════════
♪  I Gotta Feeling - The Black Eyed Peas  ♪
════════════════════════════════════════════════════════════


[Lyrics appear here after 2 seconds]
```

## How It Works

### 1. Song Name Extraction

- Automatically extracts song name from the audio file name
- Converts underscores and hyphens to spaces
- Capitalizes each word (Title Case)

**Examples:**

- `i-gotta-feeling.mp3` → "I Gotta Feeling"
- `the_black_eyed_peas.mp3` → "The Black Eyed Peas"
- `sample_song.wav` → "Sample Song"

### 2. Header Display

- Clears the screen
- Shows decorative lines (═══)
- Displays song name with music notes (♪)
- Centers everything
- Waits 2 seconds before starting playback

### 3. Color Scheme

- **Decorative lines**: Bold Magenta
- **Song name**: Bold Yellow
- **Music notes**: Bold Yellow

## Implementation

### display.py

Added `show_song_header()` method:

```python
def show_song_header(self, song_name: str) -> None:
    # Creates decorative header
    # Centers and displays with colors
    # Adds spacing for readability
```

### main.py

Updated `start_playback()`:

```python
# Extract song name from file path
song_name = self.song_path.stem.replace('_', ' ').replace('-', ' ').title()

# Show header
self.display.show_song_header(song_name)

# Wait 2 seconds
time.sleep(2)

# Start playback
```

## Benefits

✅ Professional appearance  
✅ User knows what song is playing  
✅ Gives time to prepare before lyrics start  
✅ Beautiful visual presentation  
✅ Automatic - no configuration needed

## Customization

You can customize the header by editing `src/display.py`:

- **Change colors**: Modify `style="bold magenta"` and `style="bold yellow"`
- **Change decorative lines**: Modify `"═" * 60`
- **Change music notes**: Modify `"♪"` to other symbols
- **Change wait time**: Modify `time.sleep(2)` in `main.py`

## Example Output

```
════════════════════════════════════════════════════════════
♪  Sample Song  ♪
════════════════════════════════════════════════════════════


                    Welcome
                    Welcome to
                    Welcome to Verse
                    Welcome to Verse Music
                    Welcome to Verse Music Player
```

Enjoy your enhanced music experience! 🎵
