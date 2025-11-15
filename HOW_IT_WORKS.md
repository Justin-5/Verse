# How Word-by-Word Display Works

## Behavior

Verse displays lyrics in a karaoke-style word-by-word manner:

### On Each Line:

1. Words appear progressively on the SAME line
2. Each new word is added to the previous words
3. The line builds up until complete

### When Moving to Next Line:

1. Screen clears
2. New line starts fresh
3. Process repeats

## Visual Example

```
Time: 0.00s
Display: "I"

Time: 0.50s
Display: "I got"

Time: 1.00s
Display: "I got my"

Time: 1.50s
Display: "I got my money"

Time: 2.00s (new line starts)
[Screen clears]
Display: "let's"

Time: 2.50s
Display: "let's spend"

Time: 3.00s
Display: "let's spend it"
```

## How It's Implemented

### 1. Word Timing Generation

- Each line is split into words
- Duration until next line is calculated
- Words are distributed evenly across that duration

### 2. Line Change Detection

- System tracks current line index
- When line index changes, display resets
- This ensures clean transitions between lines

### 3. Progressive Display

- `get_current_words()` returns all words up to current time
- Words accumulate on the same line
- Display updates every 50ms for smooth transitions

## Code Flow

```python
# In main.py _sync_loop():
1. Get current timestamp
2. Check if we moved to a new line
3. If new line: reset display
4. Get accumulated words for current line
5. Display the words
6. Repeat every 50ms
```

## Result

You get a smooth karaoke experience where:

- ✅ Words appear one by one on the same line
- ✅ Line builds up progressively
- ✅ Clean transition to next line
- ✅ No repetition across lines
- ✅ Synchronized with music

This is exactly how karaoke systems work!
