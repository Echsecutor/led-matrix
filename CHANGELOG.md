# LED Matrix Project Changelog

## WIP

- Added new interactive text display script `text_display.py`
  - Interactive mode prompts user for text input and display mode selection
  - Command line mode supports direct text input via `-t/--text` parameter
  - Three display modes available:
    - Vertical scroll (default): Text scrolls vertically using `show_message`
    - Horizontal scroll: Text scrolls horizontally using custom viewport
    - Static display: Text displays statically for 5 seconds
  - Configurable logging levels via `-l/--log` parameter
  - Uses same hardware configuration as existing scripts (4x8x8 LED matrices)
  - Proper error handling and keyboard interrupt support
  - Clean exit with device clearing
- Fixed input handling in `text_display.py`
  - Added Python 3 requirement check and explicit shebang
  - Improved input error handling with try/catch blocks for `EOFError` and `KeyboardInterrupt`
  - Fixed `NameError` issue when entering text input
