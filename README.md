# 1.54 inch LCD GAME Driver for CM4

Драйвер для 1.54 inch LCD GAME дисплея на Raspberry Pi CM4 с подключением через 40PIN гребенку.

## Описание

Этот проект содержит драйвер и инструкции для подключения и настройки 1.54 inch LCD GAME дисплея (ST7789) к Raspberry Pi CM4 через 40PIN гребенку.

## Характеристики дисплея

- **Разрешение**: 240x240 пикселей
- **Контроллер**: ST7789
- **Интерфейс**: SPI
- **Сенсор**: Capacitive touch (если поддерживается)
- **Размер**: 1.54 inch

## Подключение к CM4

### Схема подключения 40PIN

| LCD Pin | CM4 Pin | Функция |
|---------|---------|---------|
| VCC     | 3.3V    | Питание |
| GND     | GND     | Земля   |
| SCL     | GPIO 11 | SPI SCLK |
| SDA     | GPIO 10 | SPI MOSI |
| RES     | GPIO 25 | Reset |
| DC      | GPIO 24 | Data/Command |
| CS      | GPIO 8  | Chip Select |
| BLK     | GPIO 18 | Backlight |

## Установка

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd cm4-lcd-game-driver
```

2. Установите зависимости:
```bash
sudo apt update
sudo apt install python3-pip python3-dev
pip3 install -r requirements.txt
```

3. Настройте SPI интерфейс:
```bash
sudo raspi-config
# Включите SPI в Interface Options
```

4. Запустите установку драйвера:
```bash
sudo ./install.sh
```

## Использование

### Базовый пример

```python
from lcd_game import LCDGame

# Инициализация дисплея
lcd = LCDGame()

# Очистка экрана
lcd.clear()

# Отображение текста
lcd.draw_text("Hello CM4!", 10, 10, color=(255, 255, 255))

# Отображение изображения
lcd.draw_image("image.png", 0, 0)

# Обновление экрана
lcd.update()
```

### Игровой пример

```python
from lcd_game import LCDGame
import time

lcd = LCDGame()

# Простая игра "Змейка"
def snake_game():
    # Инициализация игры
    snake = [(120, 120)]
    direction = (1, 0)
    food = (100, 100)
    
    while True:
        # Обработка ввода
        # Логика игры
        # Отрисовка
        lcd.clear()
        lcd.draw_rect(food[0], food[1], 5, 5, color=(255, 0, 0))
        for segment in snake:
            lcd.draw_rect(segment[0], segment[1], 5, 5, color=(0, 255, 0))
        lcd.update()
        time.sleep(0.1)

snake_game()
```

## Конфигурация

Основные настройки можно изменить в файле `config.py`:

```python
# Настройки SPI
SPI_BUS = 0
SPI_DEVICE = 0
SPI_SPEED = 40000000

# Настройки дисплея
DISPLAY_WIDTH = 240
DISPLAY_HEIGHT = 240
ROTATION = 0

# Настройки пинов
PIN_RESET = 25
PIN_DC = 24
PIN_CS = 8
PIN_BACKLIGHT = 18
```

## Устранение неполадок

### Дисплей не включается
1. Проверьте подключение питания (3.3V)
2. Убедитесь, что SPI включен в raspi-config
3. Проверьте правильность подключения пинов

### Нет изображения
1. Проверьте подключение пинов SCL, SDA, RES, DC, CS
2. Убедитесь, что драйвер установлен корректно
3. Проверьте логи: `dmesg | grep spi`

### Медленная работа
1. Уменьшите скорость SPI в config.py
2. Оптимизируйте код отрисовки
3. Используйте аппаратное ускорение

## Лицензия

MIT License

## Поддержка

При возникновении проблем создайте issue в репозитории или обратитесь к документации.