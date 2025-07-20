# SHIWA NETWORK Grand Mini - CM4 LCD System

Полнофункциональная система для Raspberry Pi CM4 с 1.54 inch LCD GAME дисплеем, включающая заставку включения, рабочий стол, игры и полный набор инструментов разработки.

## 🎯 Описание проекта

Этот проект представляет собой комплексную систему для CM4 с LCD дисплеем, включающую:

- **Драйвер дисплея** - полная поддержка ST7789 контроллера
- **Заставка включения** - анимированная загрузка системы
- **Рабочий стол** - интерактивный интерфейс с меню
- **Игровой движок** - для создания игр и приложений
- **Система тестирования** - проверка всех компонентов
- **Автоматическая установка** - полная настройка системы

## 📋 Характеристики дисплея

- **Разрешение**: 240x240 пикселей
- **Контроллер**: ST7789
- **Интерфейс**: SPI
- **Цветовая глубина**: 16-bit (RGB565)
- **Размер**: 1.54 inch
- **Подсветка**: Управляемая

## 🔌 Подключение к CM4

### Схема подключения 40PIN

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

## 🚀 Быстрая установка

### 1. Клонирование и установка
```bash
git clone <repository-url>
cd cm4-lcd-game-driver
sudo ./install.sh
sudo reboot
```

### 2. Тестирование системы
```bash
sudo python3 test_system.py
```

### 3. Запуск системы
```bash
sudo python3 main.py
```

## 🎮 Использование

### Запуск полной системы

```bash
# Запуск системы с заставкой и рабочим столом
sudo python3 main.py
```

Система автоматически:
1. Показывает анимированную заставку включения
2. Загружает рабочий стол с меню
3. Предоставляет доступ к играм и настройкам

### Базовое использование драйвера

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

### Создание игры

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

## 📁 Структура проекта

```
cm4-lcd-game-driver/
├── README.md                 # Основная документация
├── main.py                   # Главная система
├── lcd_game.py              # Драйвер дисплея
├── boot_splash.py           # Заставка включения
├── desktop.py               # Рабочий стол
├── test_system.py           # Тестирование системы
├── config.py                # Конфигурация
├── install.sh               # Автоматическая установка
├── requirements.txt         # Python зависимости
├── examples/                # Примеры использования
│   ├── demo.py             # Демонстрация возможностей
│   ├── snake_game.py       # Игра "Змейка"
│   ├── simple_game.py      # Простая игра
│   └── button_test.py      # Тест кнопок
├── docs/                   # Документация
│   ├── WIRING_GUIDE.md     # Инструкция по подключению
│   └── PINOUT_GUIDE.md     # Схема распиновки
├── CHANGELOG.md            # История изменений
├── PROJECT_OVERVIEW.md     # Обзор проекта
├── QUICK_START.md          # Быстрый старт
└── SYSTEM_README.md        # Системная документация
```

## 🎯 Основные компоненты

### 1. Главная система (`main.py`)
- Объединяет все компоненты системы
- Управляет жизненным циклом приложения
- Обработка сигналов и корректное завершение

### 2. Драйвер дисплея (`lcd_game.py`)
- Инициализация ST7789 контроллера
- SPI интерфейс для CM4
- Рисование примитивов (линии, прямоугольники, круги)
- Отображение текста с различными шрифтами
- Управление подсветкой
- Игровой движок для создания игр

### 3. Заставка включения (`boot_splash.py`)
- Анимированная загрузка системы
- Логотип SHIWA NETWORK Grand Mini
- Прогресс-бар загрузки
- Пульсирующие эффекты

### 4. Рабочий стол (`desktop.py`)
- Интерактивный интерфейс
- Системная информация (CPU, RAM, температура)
- Меню приложений
- Настройки системы
- Сетевой статус

### 5. Система тестирования (`test_system.py`)
- Проверка LCD дисплея
- Тест кнопок управления
- Тест заставки включения
- Тест рабочего стола
- Автоматическая диагностика

## 🎮 Примеры и игры

### Демонстрация возможностей
```bash
sudo python3 examples/demo.py
```

### Игра "Змейка"
```bash
sudo python3 examples/snake_game.py
```

### Простая игра
```bash
sudo python3 examples/simple_game.py
```

### Тест кнопок
```bash
sudo python3 examples/button_test.py
```

## ⚙️ Конфигурация

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

# Настройки пинов дисплея
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

## 🔧 Управление системой

### Автоматический запуск
```bash
# Включение автозапуска
sudo systemctl enable lcd-game

# Запуск сервиса
sudo systemctl start lcd-game

# Проверка статуса
sudo systemctl status lcd-game

# Остановка сервиса
sudo systemctl stop lcd-game
```

### Ручной запуск
```bash
# Запуск полной системы
sudo python3 main.py

# Только тестирование
sudo python3 test_system.py

# Демонстрация
sudo python3 examples/demo.py
```

## 🛠️ Устранение неполадок

### Дисплей не включается
1. Проверьте подключение питания (3.3V)
2. Убедитесь, что SPI включен в raspi-config
3. Проверьте правильность подключения пинов
4. Запустите тест: `sudo python3 test_system.py`

### Нет изображения
1. Проверьте подключение пинов SCL, SDA, RES, DC, CS
2. Убедитесь, что драйвер установлен корректно
3. Проверьте логи: `dmesg | grep spi`
4. Проверьте права доступа: `sudo python3 main.py`

### Кнопки не работают
1. Проверьте подключение кнопок к соответствующим GPIO
2. Убедитесь, что используется правильная нумерация (BCM)
3. Проверьте подтягивающие резисторы
4. Запустите тест кнопок: `sudo python3 examples/button_test.py`

### Медленная работа
1. Уменьшите скорость SPI в config.py
2. Оптимизируйте код отрисовки
3. Используйте аппаратное ускорение
4. Проверьте качество соединений

### Проблемы с системой
1. Проверьте все зависимости: `pip3 install -r requirements.txt`
2. Перезапустите систему: `sudo reboot`
3. Проверьте логи: `sudo journalctl -u lcd-game -f`
4. Запустите полное тестирование: `sudo python3 test_system.py`

## 📚 Документация

- **QUICK_START.md** - Быстрый старт
- **PROJECT_OVERVIEW.md** - Подробный обзор проекта
- **SYSTEM_README.md** - Системная документация
- **docs/WIRING_GUIDE.md** - Инструкция по подключению
- **docs/PINOUT_GUIDE.md** - Схема распиновки
- **CHANGELOG.md** - История изменений

## 🎯 Возможности системы

### ✅ Реализовано
- Полный драйвер ST7789 контроллера
- Анимированная заставка включения
- Интерактивный рабочий стол
- Игровой движок для создания игр
- Система тестирования всех компонентов
- Автоматическая установка и настройка
- Поддержка всех кнопок управления
- Демонстрационные примеры и игры
- Подробная документация

### 🔄 В разработке
- Поддержка сенсорного ввода
- Дополнительные игровые примеры
- Веб-интерфейс для настройки
- Сетевые функции

## 📄 Лицензия

MIT License - см. файл `LICENSE` для подробностей.

## 🤝 Поддержка

При возникновении проблем:
1. Запустите тестирование: `sudo python3 test_system.py`
2. Проверьте документацию в папке `docs/`
3. Создайте issue в репозитории
4. Обратитесь к руководству по устранению неполадок

---

**SHIWA NETWORK Grand Mini** - Полнофункциональная система для CM4 с LCD дисплеем