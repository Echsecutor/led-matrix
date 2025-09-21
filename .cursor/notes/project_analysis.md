# LED Matrix Project Analysis

## Hardware Setup

- **Device**: MAX7219 LED matrix controller
- **Configuration**: 4 cascaded 8x8 LED matrices (32x8 total resolution)
- **Connection**: SPI interface (port=0, device=0)
- **Orientation**: -90° block orientation, 180° rotation, monochrome mode

## Main Scripts

### good_morning_LED.py

**Purpose**: Interactive display with multiple information screens

**Key Features**:

- Weather display via OpenWeatherMap API (Cologne location)
- Time-based greetings (German language)
- Current time and date display
- Image display capabilities (local files and URLs)
- Scrolling text animations (horizontal and vertical)

**Display Functions**:

- `show_weather()` - Weather icon and temperature
- `show_greetings()` - Time-based German greetings
- `show_time()` - Current time (HH:MM format)
- `show_date()` - Current date (DD.MM format)
- `vertical_scroll()` - Vertical scrolling text
- `horizontal_scroll_msg()` - Horizontal scrolling text
- `display_img()` - Image display with scaling

**Configuration**:

- Requires OpenWeatherMap API token via command line argument
- Configurable logging levels
- Low contrast setting (device.contrast(0))

### sleep_clock.py

**Purpose**: Simple clock with night mode

**Features**:

- Displays current time (HH:MM)
- Auto-hides between 22:00-06:00
- Sleeps until next hour during night mode
- Minimal resource usage

## Dependencies

- `luma.led_matrix` - LED matrix control library
- `luma.core` - Core display functionality
- `PIL` (Pillow) - Image processing
- `requests` - HTTP requests for weather API
- Standard library: `time`, `logging`, `os`, `argparse`

## API Integration

- OpenWeatherMap API for weather data
- Requires API token for functionality
- Fetches weather for Cologne, Germany
- Downloads weather icons dynamically

## Error Handling

- Keyboard interrupt handling for clean shutdown
- Exception logging in main loop
- Graceful degradation on API failures
