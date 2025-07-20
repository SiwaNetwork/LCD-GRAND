# Быстрый старт - 1.54 inch LCD GAME на CM4

## Быстрая установка

### 1. Клонирование репозитория
```bash
git clone <repository-url>
cd cm4-lcd-game-driver
```

### 2. Установка драйвера
```bash
sudo ./install.sh
```

### 3. Перезагрузка системы
```bash
sudo reboot
```

### 4. Тестирование
```bash
# Базовый тест
sudo /opt/lcd_game_driver/test_display.py

# Демонстрация возможностей
sudo python3 examples/demo.py

# Игра "Змейка"
sudo python3 examples/snake_game.py
```

## Подключение дисплея

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

## Базовое использование

### Простой пример
```python
from lcd_game import LCDGame

# Инициализация дисплея
lcd = LCDGame()

# Очистка экрана
lcd.clear()

# Рисование текста
lcd.draw_text("Hello CM4!", 10, 10, color=(255, 255, 255))

# Рисование фигур
lcd.draw_rect(50, 50, 100, 50, color=(255, 0, 0), fill=True)
lcd.draw_circle(150, 150, 30, color=(0, 255, 0), fill=True)

# Обновление дисплея
lcd.update()
```

### Игровой пример
```python
from lcd_game import LCDGame, GameEngine

class MyGame(GameEngine):
    def update(self, delta_time):
        # Обновление игровой логики
        pass
    
    def render(self):
        # Отрисовка
        self.lcd.clear()
        self.lcd.draw_text("Game Running", 10, 10)
        self.lcd.update()

# Запуск игры
game = MyGame(LCDGame())
game.start()
```

## Управление сервисом

```bash
# Запуск сервиса
sudo systemctl start lcd-game

# Остановка сервиса
sudo systemctl stop lcd-game

# Автозапуск
sudo systemctl enable lcd-game

# Статус сервиса
sudo systemctl status lcd-game
```

## Устранение неполадок

### Дисплей не работает
1. Проверьте подключение пинов
2. Убедитесь, что SPI включен: `sudo raspi-config`
3. Проверьте права доступа: `sudo usermod -a -G spi $USER`

### Нет изображения
1. Проверьте логи: `sudo journalctl -u lcd-game -f`
2. Проверьте SPI: `ls /dev/spidev*`
3. Перезагрузите систему: `sudo reboot`

### Медленная работа
1. Уменьшите скорость SPI в `config.py`
2. Оптимизируйте код отрисовки
3. Используйте аппаратное ускорение

## Дополнительная документация

- [Подробная инструкция по подключению](docs/WIRING_GUIDE.md)
- [Примеры использования](examples/)
- [Конфигурация](config.py)
- [API документация](lcd_game.py)

## Поддержка

При возникновении проблем:
1. Проверьте раздел "Устранение неполадок"
2. Обратитесь к документации
3. Создайте issue в репозитории