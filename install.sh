#!/bin/bash

# Скрипт установки драйвера для 1.54 inch LCD GAME на CM4
# Автор: CM4 LCD Game Driver Team
# Версия: 1.0

set -e

echo "=========================================="
echo "Установка драйвера 1.54 inch LCD GAME"
echo "для Raspberry Pi CM4"
echo "=========================================="

# Проверка прав администратора
if [ "$EUID" -ne 0 ]; then
    echo "Ошибка: Этот скрипт должен быть запущен с правами администратора"
    echo "Используйте: sudo ./install.sh"
    exit 1
fi

# Проверка системы
echo "Проверка системы..."
if ! grep -q "Raspberry Pi" /proc/cpuinfo; then
    echo "Предупреждение: Система не определена как Raspberry Pi"
    read -p "Продолжить установку? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Обновление системы
echo "Обновление системы..."
apt update
apt upgrade -y

# Установка необходимых пакетов
echo "Установка системных зависимостей..."
apt install -y \
    python3-pip \
    python3-dev \
    python3-venv \
    git \
    build-essential \
    cmake \
    pkg-config \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    libv4l-dev \
    libxvidcore-dev \
    libx264-dev \
    libgtk-3-dev \
    libatlas-base-dev \
    gfortran \
    libhdf5-dev \
    libhdf5-serial-dev \
    libhdf5-103 \
    libqtgui4 \
    libqtwebkit4 \
    libqt4-test \
    python3-pyqt5 \
    libatlas-base-dev \
    libjasper-dev \
    libqtcore4 \
    libqt4-test

# Включение SPI интерфейса
echo "Настройка SPI интерфейса..."
if ! grep -q "dtparam=spi=on" /boot/config.txt; then
    echo "dtparam=spi=on" >> /boot/config.txt
    echo "SPI интерфейс включен в /boot/config.txt"
else
    echo "SPI интерфейс уже включен"
fi

# Включение I2C интерфейса (для будущих функций)
echo "Настройка I2C интерфейса..."
if ! grep -q "dtparam=i2c_arm=on" /boot/config.txt; then
    echo "dtparam=i2c_arm=on" >> /boot/config.txt
    echo "I2C интерфейс включен в /boot/config.txt"
else
    echo "I2C интерфейс уже включен"
fi

# Создание виртуального окружения Python
echo "Создание виртуального окружения..."
python3 -m venv /opt/lcd_game_env
source /opt/lcd_game_env/bin/activate

# Установка Python зависимостей
echo "Установка Python зависимостей..."
pip3 install --upgrade pip
pip3 install -r requirements.txt

# Создание системного сервиса
echo "Создание системного сервиса..."
cat > /etc/systemd/system/lcd-game.service << EOF
[Unit]
Description=LCD Game Driver Service
After=network.target

[Service]
Type=simple
User=pi
Group=pi
WorkingDirectory=/opt/lcd_game_driver
Environment=PATH=/opt/lcd_game_env/bin
ExecStart=/opt/lcd_game_env/bin/python3 /opt/lcd_game_driver/lcd_game.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Копирование файлов в системную директорию
echo "Копирование файлов..."
mkdir -p /opt/lcd_game_driver
cp *.py /opt/lcd_game_driver/
cp requirements.txt /opt/lcd_game_driver/
chown -R pi:pi /opt/lcd_game_driver
chmod +x /opt/lcd_game_driver/*.py

# Создание символических ссылок
echo "Создание символических ссылок..."
ln -sf /opt/lcd_game_driver/lcd_game.py /usr/local/bin/lcd-game
chmod +x /usr/local/bin/lcd-game

# Создание конфигурационного файла
echo "Создание конфигурационного файла..."
cat > /etc/lcd_game.conf << EOF
# Конфигурация LCD Game Driver
[display]
width = 240
height = 240
rotation = 0
brightness = 100

[spi]
bus = 0
device = 0
speed = 40000000

[gpio]
reset = 25
dc = 24
cs = 8
backlight = 18

[performance]
fps = 30
buffer_size = 1024
EOF

# Создание директории для логов
echo "Создание директории для логов..."
mkdir -p /var/log/lcd_game
chown pi:pi /var/log/lcd_game

# Создание тестового скрипта
echo "Создание тестового скрипта..."
cat > /opt/lcd_game_driver/test_display.py << 'EOF'
#!/usr/bin/env python3
"""
Тестовый скрипт для проверки работы LCD дисплея
"""

import sys
import time
from lcd_game import LCDGame

def test_display():
    """Тестирование дисплея"""
    try:
        print("Инициализация LCD дисплея...")
        lcd = LCDGame()
        
        print("Очистка экрана...")
        lcd.clear()
        
        print("Рисование тестового изображения...")
        # Рисование цветных прямоугольников
        lcd.draw_rect(10, 10, 50, 50, color=(255, 0, 0), fill=True)  # Красный
        lcd.draw_rect(70, 10, 50, 50, color=(0, 255, 0), fill=True)   # Зеленый
        lcd.draw_rect(130, 10, 50, 50, color=(0, 0, 255), fill=True)  # Синий
        
        # Рисование текста
        lcd.draw_text("LCD Test", 10, 80, color=(255, 255, 255), font_size=16)
        lcd.draw_text("CM4 Ready!", 10, 100, color=(255, 255, 0), font_size=12)
        
        # Рисование кругов
        lcd.draw_circle(60, 150, 20, color=(255, 0, 255), fill=True)
        lcd.draw_circle(120, 150, 20, color=(0, 255, 255), fill=True)
        lcd.draw_circle(180, 150, 20, color=(255, 255, 0), fill=True)
        
        # Обновление дисплея
        lcd.update()
        
        print("Тест завершен успешно!")
        print("Нажмите Ctrl+C для выхода...")
        
        # Ожидание
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nЗавершение теста...")
        lcd.cleanup()
    except Exception as e:
        print(f"Ошибка тестирования: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_display()
EOF

chmod +x /opt/lcd_game_driver/test_display.py

# Создание документации
echo "Создание документации..."
mkdir -p /opt/lcd_game_driver/docs
cat > /opt/lcd_game_driver/docs/QUICK_START.md << 'EOF'
# Быстрый старт

## Запуск теста дисплея
```bash
sudo /opt/lcd_game_driver/test_display.py
```

## Запуск основного драйвера
```bash
sudo lcd-game
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

## Примеры использования

### Базовый пример
```python
from lcd_game import LCDGame

lcd = LCDGame()
lcd.clear()
lcd.draw_text("Hello World!", 10, 10)
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

game = MyGame(LCDGame())
game.start()
```
EOF

# Перезагрузка systemd
echo "Перезагрузка systemd..."
systemctl daemon-reload

# Включение автозапуска сервиса
echo "Включение автозапуска сервиса..."
systemctl enable lcd-game.service

echo "=========================================="
echo "Установка завершена успешно!"
echo "=========================================="
echo ""
echo "Для тестирования дисплея выполните:"
echo "sudo /opt/lcd_game_driver/test_display.py"
echo ""
echo "Для запуска сервиса выполните:"
echo "sudo systemctl start lcd-game"
echo ""
echo "Для просмотра статуса:"
echo "sudo systemctl status lcd-game"
echo ""
echo "Документация находится в:"
echo "/opt/lcd_game_driver/docs/"
echo ""
echo "Перезагрузите систему для применения всех изменений:"
echo "sudo reboot"
echo "=========================================="