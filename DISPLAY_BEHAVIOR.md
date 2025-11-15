# Display Behavior - Word-by-Word on Same Line

## How It Works Now

### Terminal Display Behavior:

**Line 1 (builds up on the SAME terminal line):**

```
I
I got
I got my
I got my money
I got my money, let's spend
```

**[Screen clears - moves to next terminal line]**

**Line 2 (builds up on the SAME terminal line):**

```
Go
Go out
Go out and
Go out and smash
Go out and smash it
```

## Technical Implementation

### Using ANSI Escape Codes

Instead of printing on a new line each time, we use ANSI escape codes to move the cursor up and clear the line:

```python
# ANSI codes:
# \033[F - Move cursor up one line
# \033[K - Clear from cursor to end of line

# This allows us to overwrite the previous line
console.file.write("\033[F\033[K")
console.print(new_text)
```

### Display Logic

1. **Within a line**: Use `\r` to overwrite and build up words
2. **New line starts**: Clear screen and start fresh
3. **Words accumulate**: Each word adds to previous words on same line

## Code Changes

### display.py

- Added `clear_line` parameter to `show_lyric()`
- Uses `end="\r"` to overwrite same line
- Only clears screen when `clear_line=True`

### main.py

- Tracks when moving to new line
- Sets `is_new_line` flag
- Passes `clear_line=True` for first word of new line
- Passes `clear_line=False` for subsequent words

## Result

✅ Words appear horizontally on the same terminal line  
✅ Each word adds to the previous words  
✅ No vertical scrolling within a line  
✅ Clean transition to next line when lyrics change  
✅ True karaoke-style display

## Visual Example

```
Terminal Line 1: "I" → "I got" → "I got my" → "I got my money"
[Clear]
Terminal Line 2: "let's" → "let's spend" → "let's spend it"
[Clear]
Terminal Line 3: "Go" → "Go out" → "Go out and" → "Go out and smash"
```

Each arrow (→) represents the same terminal line being overwritten with more words!
