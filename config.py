# Конфигурация для 1.54 inch LCD GAME дисплея на CM4

# Настройки SPI
SPI_BUS = 0
SPI_DEVICE = 0
SPI_SPEED = 40000000  # 40 MHz

# Настройки дисплея
DISPLAY_WIDTH = 240
DISPLAY_HEIGHT = 240
ROTATION = 0

# Настройки пинов GPIO (BCM нумерация)
PIN_RESET = 25      # GPIO 25 - Reset
PIN_DC = 24         # GPIO 24 - Data/Command
PIN_CS = 8          # GPIO 8  - Chip Select
PIN_BACKLIGHT = 18  # GPIO 18 - Backlight

# Настройки цветов (RGB)
COLORS = {
    'BLACK': (0, 0, 0),
    'WHITE': (255, 255, 255),
    'RED': (255, 0, 0),
    'GREEN': (0, 255, 0),
    'BLUE': (0, 0, 255),
    'YELLOW': (255, 255, 0),
    'CYAN': (0, 255, 255),
    'MAGENTA': (255, 0, 255),
    'GRAY': (128, 128, 128),
    'DARK_GRAY': (64, 64, 64),
    'LIGHT_GRAY': (192, 192, 192)
}

# Настройки шрифтов
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
DEFAULT_FONT_SIZE = 12

# Настройки игрового движка
DEFAULT_FPS = 30
MAX_FPS = 60

# Настройки отладки
DEBUG = False
LOG_LEVEL = "INFO"

# Настройки производительности
BUFFER_SIZE = 1024
DMA_CHANNEL = 0

# Настройки энергосбережения
BACKLIGHT_TIMEOUT = 300  # секунды
SLEEP_TIMEOUT = 600      # секунды

# Настройки калибровки сенсора (если поддерживается)
TOUCH_CALIBRATION = {
    'x_min': 0,
    'x_max': 240,
    'y_min': 0,
    'y_max': 240,
    'rotation': 0
}

# Настройки инициализации ST7789
ST7789_INIT_COMMANDS = [
    (0x11, None),  # Sleep out
    (0x36, [0x00]),  # Memory Access Control
    (0x3A, [0x05]),  # Interface Pixel Format
    (0x2A, [0x00, 0x00, 0x00, 0xEF]),  # Column Address Set
    (0x2B, [0x00, 0x00, 0x00, 0xEF]),  # Row Address Set
    (0x2C, None),  # Memory Write
    (0xB2, [0x0C, 0x0C, 0x00, 0x33, 0x33]),  # Porch Setting
    (0xB7, [0x35]),  # Gate Control
    (0xBB, [0x19]),  # VCOM Setting
    (0xC0, [0x2C]),  # LCM Control
    (0xC2, [0x01]),  # VDV and VRH Command Enable
    (0xC3, [0x12]),  # VRH Set
    (0xC4, [0x20]),  # VDV Set
    (0xC6, [0x0F]),  # Frame Rate Control in Normal Mode
    (0xD0, [0xA4, 0xA1]),  # Power Control 1
    (0xE0, [0xD0, 0x04, 0x0D, 0x11, 0x13, 0x2B, 0x3F, 0x54, 0x4C, 0x18, 0x0D, 0x0B, 0x1F, 0x23]),  # Positive Voltage Gamma Control
    (0xE1, [0xD0, 0x04, 0x0C, 0x11, 0x13, 0x2C, 0x3F, 0x44, 0x51, 0x2F, 0x1F, 0x1F, 0x20, 0x23]),  # Negative Voltage Gamma Control
    (0x21, None),  # Display Inversion On
    (0x29, None),  # Display On
]

# Настройки для разных режимов работы
DISPLAY_MODES = {
    'NORMAL': {
        'brightness': 100,
        'contrast': 100,
        'gamma': 1.0
    },
    'GAMING': {
        'brightness': 80,
        'contrast': 120,
        'gamma': 1.2
    },
    'BATTERY_SAVE': {
        'brightness': 50,
        'contrast': 80,
        'gamma': 0.8
    }
}