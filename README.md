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

### Схема подключения 40PIN (обновлено согласно распиновке)

| LCD Pin | CM4 Pin | GPIO (BCM) | Функция |
|---------|---------|------------|---------|
| VCC     | Pin 1, 17 | - | Питание 3.3V |
| GND     | Pin 6, 9, 14, 20, 25, 30, 34, 39 | - | Земля |
| SCL     | Pin 23 | GPIO 11 | SPI SCLK |
| SDA     | Pin 19 | GPIO 10 | SPI MOSI |
| RES     | Pin 13 | GPIO 27 | Reset |
| DC      | Pin 15 | GPIO 22 | Data/Command |
| CS      | Pin 24 | GPIO 8  | Chip Select |
| BLK     | Pin 12 | GPIO 18 | Backlight |

### Кнопки управления

| Кнопка | CM4 Pin | GPIO (BCM) | Функция |
|--------|---------|------------|---------|
| A      | Pin 40 | GPIO 21 | Кнопка A |
| B      | Pin 38 | GPIO 20 | Кнопка B |
| UP     | Pin 36 | GPIO 16 | Кнопка вверх |
| DOWN   | Pin 29 | GPIO 5  | Кнопка вниз |
| LEFT   | Pin 31 | GPIO 6  | Кнопка влево |
| RIGHT  | Pin 33 | GPIO 13 | Кнопка вправо |
| START  | Pin 35 | GPIO 19 | Кнопка старт |
| SELECT | Pin 37 | GPIO 26 | Кнопка селект |
| MENU   | Pin 11 | GPIO 17 | Кнопка меню |

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

### Игровой пример с кнопками

```python
from lcd_game import LCDGame, GameEngine
import time

class SimpleGame(GameEngine):
    def __init__(self, lcd):
        super().__init__(lcd)
        self.player_x = 120
        self.player_y = 120
        self.score = 0
    
    def handle_input(self):
        # Движение игрока
        if self.lcd.buttons.is_held('UP'):
            self.player_y = max(10, self.player_y - 3)
        if self.lcd.buttons.is_held('DOWN'):
            self.player_y = min(230, self.player_y + 3)
        if self.lcd.buttons.is_held('LEFT'):
            self.player_x = max(10, self.player_x - 3)
        if self.lcd.buttons.is_held('RIGHT'):
            self.player_x = min(230, self.player_x + 3)
        
        # Действия кнопок
        if self.lcd.buttons.is_pressed('A'):
            self.score += 10
        if self.lcd.buttons.is_pressed('B'):
            self.score += 5
    
    def render(self):
        self.lcd.clear()
        self.lcd.draw_circle(self.player_x, self.player_y, 10, color=(0, 255, 0), fill=True)
        self.lcd.draw_text(f"Score: {self.score}", 10, 10, color=(255, 255, 255))
        self.lcd.update()

# Запуск игры
lcd = LCDGame()
game = SimpleGame(lcd)
game.start()
```

### Тест кнопок

```python
from lcd_game import LCDGame
import time

lcd = LCDGame()

while True:
    # Проверка нажатий кнопок
    for button_name in ['A', 'B', 'UP', 'DOWN', 'LEFT', 'RIGHT', 'START', 'SELECT']:
        if lcd.buttons.is_pressed(button_name):
            print(f"Кнопка {button_name} нажата!")
    
    time.sleep(0.1)
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

# Настройки пинов дисплея (обновлено согласно схеме)
PIN_RESET = 27      # GPIO 27 (Pin 13)
PIN_DC = 22         # GPIO 22 (Pin 15)
PIN_CS = 8          # GPIO 8  (Pin 24)
PIN_BACKLIGHT = 18  # GPIO 18 (Pin 12)

# Настройки кнопок
BUTTON_PINS = {
    'A': 21,        # GPIO 21 (Pin 40)
    'B': 20,        # GPIO 20 (Pin 38)
    'UP': 16,       # GPIO 16 (Pin 36)
    'DOWN': 5,      # GPIO 5  (Pin 29)
    'LEFT': 6,      # GPIO 6  (Pin 31)
    'RIGHT': 13,    # GPIO 13 (Pin 33)
    'START': 19,    # GPIO 19 (Pin 35)
    'SELECT': 26,   # GPIO 26 (Pin 37)
    'MENU': 17,     # GPIO 17 (Pin 11)
}
```

## Примеры

В папке `examples/` находятся готовые примеры:

- `button_test.py` - Тест всех кнопок
- `simple_game.py` - Простая игра с управлением кнопками

Запуск примеров:
```bash
# Тест кнопок
python3 examples/button_test.py

# Простая игра
python3 examples/simple_game.py
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

### Кнопки не работают
1. Проверьте подключение кнопок к соответствующим GPIO
2. Убедитесь, что используется правильная нумерация (BCM)
3. Проверьте подтягивающие резисторы

### Медленная работа
1. Уменьшите скорость SPI в config.py
2. Оптимизируйте код отрисовки
3. Используйте аппаратное ускорение

## Лицензия

MIT License

## Поддержка

При возникновении проблем создайте issue в репозитории или обратитесь к документации.