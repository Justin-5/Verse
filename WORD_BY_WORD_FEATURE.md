# Word-by-Word Karaoke Feature

Verse now supports word-by-word lyric display for a true karaoke experience!

## How It Works

Instead of showing the entire line at once, Verse displays words one by one as they should be sung. The timing is automatically calculated based on:

1. The timestamp of the current line
2. The timestamp of the next line
3. The number of words in the line

Words are distributed evenly across the available time.

## Example

For a line like:

```lrc
[00:00.00]Welcome to Verse Music Player
[00:03.50]This is a sample song
```

The words will appear progressively:

- 0.00s: "Welcome"
- 0.70s: "Welcome to"
- 1.40s: "Welcome to Verse"
- 2.10s: "Welcome to Verse Music"
- 2.80s: "Welcome to Verse Music Player"

## Automatic Timing

The system automatically:

- Splits each line into words
- Calculates the duration until the next line
- Distributes words evenly across that duration
- Displays words progressively as the song plays

## Technical Details

### Word Timing Calculation

```python
duration = next_line_timestamp - current_line_timestamp
time_per_word = duration / number_of_words
word_timestamp = line_timestamp + (word_index * time_per_word)
```

### Display Update Rate

- Updates every 50ms (0.05 seconds) for smooth word transitions
- More responsive than line-by-line mode (which used 100ms)

## Benefits

✅ True karaoke experience  
✅ Easier to follow along while singing  
✅ More engaging visual feedback  
✅ Automatic - no special LRC format needed  
✅ Works with any standard LRC file

## Limitations

- Word timing is evenly distributed (not based on actual singing)
- Works best with lines that have consistent word pacing
- Very fast or slow sections may not be perfectly timed

## Future Enhancements

Potential improvements:

- Support for word-level timestamps in LRC files (Enhanced LRC format)
- Adjustable word timing speed
- Toggle between word-by-word and line-by-line modes
- Highlight current word in different color
- Syllable-level timing for even more precision

## Comparison

### Line-by-Line Mode (Old)

```
[Shows entire line at once]
Welcome to Verse Music Player
```

### Word-by-Word Mode (New)

```
[Shows words progressively]
Welcome
Welcome to
Welcome to Verse
Welcome to Verse Music
Welcome to Verse Music Player
```

Enjoy the enhanced karaoke experience! 🎤
