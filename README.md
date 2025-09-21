# LED Matrix Display Project

A Python project for displaying information on a Raspberry Pi connected LED matrix array. Features weather information, time-based greetings, and clock functionality.

## Hardware Requirements

- Raspberry Pi (any model with SPI support)
- 4x MAX7219 LED matrix modules (8x8 each, creating a 32x8 display)
- SPI connection between Raspberry Pi and LED matrices

## Features

### Main Display Script (`good_morning_LED.py`)

- **Weather Display**: Shows current weather conditions and temperature for Cologne, Germany
- **Smart Greetings**: Time-aware German greetings throughout the day
- **Time & Date**: Current time (HH:MM) and date (DD.MM) display
- **Image Support**: Display images from local files or URLs with automatic scaling
- **Scrolling Animations**: Both horizontal and vertical text scrolling

### Sleep Clock (`sleep_clock.py`)

- **Simple Clock**: Displays current time in HH:MM format
- **Night Mode**: Automatically hides display between 22:00-06:00
- **Energy Efficient**: Sleeps during night hours to save power

## Installation

1. **Install Dependencies**:

   ```bash
   pip install luma.led_matrix pillow requests
   ```

2. **Hardware Setup**:

   - Connect LED matrices via SPI (port 0, device 0)
   - Ensure proper power supply for LED matrices
   - Configure matrices in cascaded arrangement

3. **API Setup** (for weather functionality):
   - Get an API token from [OpenWeatherMap](https://openweathermap.org/api)
   - Pass the token when running the main script

## Usage

### Main Display Script

```bash
# Basic usage with weather API
python good_morning_LED.py --API_TOKEN your_openweathermap_token

# With debug logging
python good_morning_LED.py --API_TOKEN your_token --log DEBUG
```

### Sleep Clock

```bash
python sleep_clock.py
```

## Command Line Options

### good_morning_LED.py

- `-a, --API_TOKEN`: OpenWeatherMap API token (required for weather display)
- `-l, --log`: Set logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

## Configuration

The LED matrix is configured with:

- **Resolution**: 32x8 pixels (4 cascaded 8x8 matrices)
- **Orientation**: -90° block orientation with 180° rotation
- **Mode**: Monochrome (1-bit)
- **Contrast**: Low (0) for comfortable viewing

## Display Cycle

The main script cycles through:

1. Time-based greeting message
2. Weather icon and temperature
3. Current time
4. Current date

Each display element includes smooth scrolling animations.

## Customization

### Changing Location

Edit line 81 in `good_morning_LED.py` to change the weather location:

```python
r = requests.get('http://api.openweathermap.org/data/2.5/weather?q=your_city&APPID=' + API_TOKEN + '&units=metric').json()
```

### Modifying Greetings

Update the `show_greetings()` function to customize messages or change language.

### Adjusting Display Cycle

Modify the `loop()` function call in `main()` to change which functions are displayed:

```python
loop(device, [show_greetings, show_weather, show_time, show_date])
```

## Troubleshooting

- **No display**: Check SPI connections and power supply
- **Weather not showing**: Verify API token and internet connection
- **Display too bright**: Adjust `device.contrast()` value (0-255)
- **Wrong orientation**: Modify `block_orientation` and `rotate` parameters

## Dependencies

- `luma.led_matrix`: LED matrix control library
- `luma.core`: Core display functionality
- `PIL` (Pillow): Image processing
- `requests`: HTTP requests for weather API
- Python standard library modules

## License

Based on original work by Richard Hull and contributors. Modified by Sebastian Schmittner.
See LICENSE.rst for details.

## Contributing

Feel free to submit issues and enhancement requests!
