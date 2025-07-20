#!/bin/bash

# Улучшенный скрипт установки драйвера для 1.54 inch LCD GAME на CM4
# Автор: CM4 LCD Game Driver Team
# Версия: 2.0 - Enhanced with system integration

set -e

echo "=========================================="
echo "Установка драйвера 1.54 inch LCD GAME"
echo "для Raspberry Pi CM4 (Enhanced)"
echo "=========================================="

# Проверка прав администратора
if [ "$EUID" -ne 0 ]; then
    echo "Ошибка: Этот скрипт должен быть запущен с правами администратора"
    echo "Используйте: sudo ./install_enhanced.sh"
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

# Создание резервной копии
echo "Создание резервной копии..."
BACKUP_DIR="/opt/lcd_game_backup/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

if [ -f /boot/config.txt ]; then
    cp /boot/config.txt "$BACKUP_DIR/"
    echo "✓ Резервная копия config.txt создана"
fi

if [ -f /etc/X11/xorg.conf.d/99-calibration.conf ]; then
    cp /etc/X11/xorg.conf.d/99-calibration.conf "$BACKUP_DIR/"
    echo "✓ Резервная копия калибровки создана"
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
    libqt4-test \
    xinput-calibrator \
    python3-xlib

# Настройка SPI интерфейса
echo "Настройка SPI интерфейса..."
if ! grep -q "dtparam=spi=on" /boot/config.txt; then
    echo "" >> /boot/config.txt
    echo "# LCD Game Driver SPI Configuration" >> /boot/config.txt
    echo "dtparam=spi=on" >> /boot/config.txt
    echo "✓ SPI интерфейс включен"
else
    echo "✓ SPI интерфейс уже включен"
fi

# Настройка GPIO подтягивающих резисторов
echo "Настройка GPIO подтягивающих резисторов..."
GPIO_PINS="6,19,5,26,13,21,20,16,17"
if ! grep -q "gpio=$GPIO_PINS=pu" /boot/config.txt; then
    echo "" >> /boot/config.txt
    echo "# LCD Game Driver GPIO Configuration" >> /boot/config.txt
    echo "gpio=$GPIO_PINS=pu" >> /boot/config.txt
    echo "✓ Подтягивающие резисторы GPIO настроены"
else
    echo "✓ Подтягивающие резисторы GPIO уже настроены"
fi

# Создание виртуального окружения Python
echo "Создание виртуального окружения..."
INSTALL_PATH="/opt/lcd_game_driver"
mkdir -p "$INSTALL_PATH"
python3 -m venv "$INSTALL_PATH/venv"
source "$INSTALL_PATH/venv/bin/activate"

# Установка Python зависимостей
echo "Установка Python зависимостей..."
pip3 install --upgrade pip
pip3 install -r requirements.txt

# Установка PyMouse
echo "Установка PyMouse..."
pip3 install PyMouse

# Копирование файлов в системную директорию
echo "Копирование файлов..."
cp *.py "$INSTALL_PATH/"
cp requirements.txt "$INSTALL_PATH/"
chown -R pi:pi "$INSTALL_PATH"
chmod +x "$INSTALL_PATH"/*.py

# Создание символических ссылок
echo "Создание символических ссылок..."
ln -sf "$INSTALL_PATH/main.py" /usr/local/bin/lcd-game
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
reset = 27
dc = 22
cs = 8
backlight = 18

[performance]
fps = 30
buffer_size = 1024

[system]
service_name = lcd-game
install_path = $INSTALL_PATH
log_path = /var/log/lcd_game
EOF

# Создание директории для логов
echo "Создание директории для логов..."
mkdir -p /var/log/lcd_game
chown pi:pi /var/log/lcd_game

# Создание systemd сервиса
echo "Создание systemd сервиса..."
cat > /etc/systemd/system/lcd-game.service << EOF
[Unit]
Description=LCD Game Driver Service
After=network.target

[Service]
Type=simple
User=pi
Group=pi
WorkingDirectory=$INSTALL_PATH
Environment=PATH=$INSTALL_PATH/venv/bin
ExecStart=$INSTALL_PATH/venv/bin/python3 $INSTALL_PATH/main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Создание эмулятора мыши
echo "Создание эмулятора мыши..."
cat > "$INSTALL_PATH/mouse_emulator.py" << 'EOF'
#!/usr/bin/env python3
"""
Эмулятор мыши для LCD Game Driver
"""

from pymouse import PyMouse
import time
import RPi.GPIO as GPIO

# Настройка GPIO
GPIO.setmode(GPIO.BCM)

# Настройка кнопок (BCM нумерация)
BUTTON_PINS = {
    'A': 21,
    'B': 20,
    'UP': 16,
    'DOWN': 5,
    'LEFT': 6,
    'RIGHT': 13,
    'START': 19,
    'SELECT': 26,
    'MENU': 17
}

# Настройка кнопок
for button_name, pin in BUTTON_PINS.items():
    GPIO.setup(pin, GPIO.IN, GPIO.PUD_UP)

def main():
    m = PyMouse()
    button_flags = {}
    
    for button_name in BUTTON_PINS.keys():
        button_flags[button_name] = False
    
    print("Эмулятор мыши запущен...")
    
    while True:
        current_pos = m.position()
        
        # Обработка кнопок
        for button_name, pin in BUTTON_PINS.items():
            if not GPIO.input(pin):  # Кнопка нажата
                if not button_flags[button_name]:
                    button_flags[button_name] = True
                    
                    if button_name in ['A', 'B']:
                        # Эмуляция клика
                        click_type = 1 if button_name == 'A' else 2
                        m.click(current_pos[0], current_pos[1], click_type)
                        print(f"Клик: {button_name}")
                    else:
                        # Эмуляция движения мыши
                        move_speed = 5
                        if button_name == 'UP':
                            m.move(current_pos[0], current_pos[1] - move_speed)
                        elif button_name == 'DOWN':
                            m.move(current_pos[0], current_pos[1] + move_speed)
                        elif button_name == 'LEFT':
                            m.move(current_pos[0] - move_speed, current_pos[1])
                        elif button_name == 'RIGHT':
                            m.move(current_pos[0] + move_speed, current_pos[1])
                        
                        print(f"Движение: {button_name}")
            
            elif button_flags[button_name]:  # Кнопка отпущена
                button_flags[button_name] = False
        
        time.sleep(0.02)  # Poll every 20ms

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nЭмулятор мыши остановлен")
        GPIO.cleanup()
EOF

chmod +x "$INSTALL_PATH/mouse_emulator.py"

# Создание автозапуска
echo "Создание автозапуска..."
AUTOSTART_DIR="/home/pi/.config/autostart"
mkdir -p "$AUTOSTART_DIR"

cat > "$AUTOSTART_DIR/lcd-game.desktop" << EOF
[Desktop Entry]
Type=Application
Name=LCD Game Driver
Comment=LCD Game Driver for CM4
Exec=$INSTALL_PATH/venv/bin/python3 $INSTALL_PATH/main.py
Terminal=false
X-GNOME-Autostart-enabled=true
EOF

chown -R pi:pi "$AUTOSTART_DIR"

# Создание скрипта поворота экрана
echo "Создание скрипта поворота экрана..."
cat > "$INSTALL_PATH/rotate_display.sh" << 'EOF'
#!/bin/bash

# Скрипт поворота экрана для LCD Game Driver

if [ "$EUID" -ne 0 ]; then
    echo "Ошибка: Требуются права администратора"
    echo "Используйте: sudo $0 [0|90|180|270]"
    exit 1
fi

if [ $# -eq 0 ]; then
    echo "Использование: sudo $0 [0|90|180|270]"
    echo "0 - поворот 0°"
    echo "90 - поворот 90°"
    echo "180 - поворот 180°"
    echo "270 - поворот 270°"
    exit 1
fi

ANGLE=$1

if [[ ! "$ANGLE" =~ ^(0|90|180|270)$ ]]; then
    echo "Ошибка: Неподдерживаемый угол поворота"
    echo "Поддерживаемые углы: 0, 90, 180, 270"
    exit 1
fi

echo "Установка поворота экрана на ${ANGLE}°..."

# Обновление config.txt
sed -i '/^display_rotate=/d' /boot/config.txt
echo "display_rotate=$ANGLE" >> /boot/config.txt

# Обновление калибровки сенсора
CALIBRATION_DIR="/etc/X11/xorg.conf.d"
mkdir -p "$CALIBRATION_DIR"

# Матрицы калибровки для разных углов
case $ANGLE in
    0)
        CALIBRATION="268 3880 227 3936"
        ;;
    90)
        CALIBRATION="227 3936 268 3880"
        ;;
    180)
        CALIBRATION="268 3880 227 3936"
        ;;
    270)
        CALIBRATION="227 3936 268 3880"
        ;;
esac

cat > "$CALIBRATION_DIR/99-calibration.conf" << CALEOF
Section "InputClass"
        Identifier      "calibration"
        MatchProduct    "ADS7846 Touchscreen"
        Option  "Calibration"   "$CALIBRATION"
        Option  "SwapAxes"      "0"
        Option "EmulateThirdButton" "1"
        Option "EmulateThirdButtonTimeout" "1000"
        Option "EmulateThirdButtonMoveThreshold" "300"
EndSection
CALEOF

echo "✓ Поворот экрана установлен на ${ANGLE}°"
echo "✓ Калибровка сенсора обновлена"
echo "Перезагрузите систему для применения изменений: sudo reboot"
EOF

chmod +x "$INSTALL_PATH/rotate_display.sh"

# Создание тестового скрипта
echo "Создание тестового скрипта..."
cat > "$INSTALL_PATH/test_display.py" << 'EOF'
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

chmod +x "$INSTALL_PATH/test_display.py"

# Создание документации
echo "Создание документации..."
mkdir -p "$INSTALL_PATH/docs"
cat > "$INSTALL_PATH/docs/QUICK_START.md" << 'EOF'
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

## Поворот экрана
```bash
# Поворот на 90°
sudo /opt/lcd_game_driver/rotate_display.sh 90

# Поворот на 180°
sudo /opt/lcd_game_driver/rotate_display.sh 180

# Поворот на 270°
sudo /opt/lcd_game_driver/rotate_display.sh 270

# Возврат к 0°
sudo /opt/lcd_game_driver/rotate_display.sh 0
```

## Эмулятор мыши
```bash
# Запуск эмулятора мыши
sudo /opt/lcd_game_driver/mouse_emulator.py
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
echo "sudo $INSTALL_PATH/test_display.py"
echo ""
echo "Для запуска сервиса выполните:"
echo "sudo systemctl start lcd-game"
echo ""
echo "Для просмотра статуса:"
echo "sudo systemctl status lcd-game"
echo ""
echo "Для поворота экрана:"
echo "sudo $INSTALL_PATH/rotate_display.sh [0|90|180|270]"
echo ""
echo "Для запуска эмулятора мыши:"
echo "sudo $INSTALL_PATH/mouse_emulator.py"
echo ""
echo "Документация находится в:"
echo "$INSTALL_PATH/docs/"
echo ""
echo "Резервная копия создана в:"
echo "$BACKUP_DIR"
echo ""
echo "Перезагрузите систему для применения всех изменений:"
echo "sudo reboot"
echo "=========================================="