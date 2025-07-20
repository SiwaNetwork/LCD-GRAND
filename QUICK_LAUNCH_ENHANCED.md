# Быстрый запуск CM4 LCD Game Driver (Enhanced)

## 🚀 Установка за 5 минут

### 1. Клонирование репозитория
```bash
git clone <repository-url>
cd cm4-lcd-game-driver
```

### 2. Установка системы
```bash
sudo ./install_enhanced.sh
sudo reboot
```

### 3. Системная интеграция
```bash
sudo python3 system_manager.py
```

### 4. Тестирование
```bash
sudo python3 test_enhanced.py
```

## 🎮 Быстрый старт

### Запуск полной системы
```bash
sudo python3 main.py
```

### Управление сервисом
```bash
# Запуск
sudo systemctl start lcd-game

# Статус
sudo systemctl status lcd-game

# Остановка
sudo systemctl stop lcd-game

# Автозапуск
sudo systemctl enable lcd-game
```

### Поворот экрана
```bash
# 90 градусов
sudo /opt/lcd_game_driver/rotate_display.sh 90

# 180 градусов
sudo /opt/lcd_game_driver/rotate_display.sh 180

# 270 градусов
sudo /opt/lcd_game_driver/rotate_display.sh 270

# Возврат к 0
sudo /opt/lcd_game_driver/rotate_display.sh 0
```

### Эмулятор мыши
```bash
sudo /opt/lcd_game_driver/mouse_emulator.py
```

## 🔧 Диагностика

### Проверка системы
```bash
# Тестирование всех компонентов
sudo python3 test_enhanced.py

# Проверка SPI
ls -la /dev/spidev*

# Проверка GPIO
python3 -c "import RPi.GPIO as GPIO; GPIO.setmode(GPIO.BCM); print('GPIO OK')"

# Проверка поворота
grep display_rotate /boot/config.txt
```

### Логи системы
```bash
# Логи сервиса
sudo journalctl -u lcd-game -f

# Системные логи
sudo dmesg | grep -i spi
sudo dmesg | grep -i gpio
```

## 📁 Структура файлов

```
/opt/lcd_game_driver/
├── main.py                 # Главный файл
├── lcd_game.py            # Драйвер дисплея
├── boot_splash.py         # Заставка
├── desktop.py             # Рабочий стол
├── system_manager.py      # Системная интеграция
├── config.py              # Конфигурация
├── mouse_emulator.py      # Эмулятор мыши
├── rotate_display.sh      # Скрипт поворота
├── test_display.py        # Тест дисплея
└── docs/                  # Документация
    └── QUICK_START.md     # Быстрый старт
```

## 🎯 Основные команды

### Управление системой
```bash
# Запуск системы
sudo python3 main.py

# Тестирование
sudo python3 test_enhanced.py

# Системная интеграция
sudo python3 system_manager.py
```

### Управление сервисом
```bash
# Запуск
sudo systemctl start lcd-game

# Остановка
sudo systemctl stop lcd-game

# Перезапуск
sudo systemctl restart lcd-game

# Статус
sudo systemctl status lcd-game

# Логи
sudo journalctl -u lcd-game -f
```

### Управление дисплеем
```bash
# Тест дисплея
sudo /opt/lcd_game_driver/test_display.py

# Поворот экрана
sudo /opt/lcd_game_driver/rotate_display.sh [0|90|180|270]

# Эмулятор мыши
sudo /opt/lcd_game_driver/mouse_emulator.py
```

## 🔧 Настройка

### Конфигурационные файлы
- `/etc/lcd_game.conf` - основная конфигурация
- `/boot/config.txt` - настройки SPI и GPIO
- `/etc/X11/xorg.conf.d/99-calibration.conf` - калибровка сенсора

### Переменные окружения
```bash
# Путь к установке
export LCD_GAME_PATH="/opt/lcd_game_driver"

# Отладка
export LCD_DEBUG="1"

# FPS
export LCD_FPS="30"
```

## 🐛 Устранение неполадок

### Проблемы с дисплеем
```bash
# Проверка SPI
ls -la /dev/spidev*

# Проверка конфигурации
grep -i spi /boot/config.txt

# Перезагрузка SPI
sudo modprobe -r spi_bcm2835
sudo modprobe spi_bcm2835
```

### Проблемы с кнопками
```bash
# Проверка GPIO
python3 -c "import RPi.GPIO as GPIO; GPIO.setmode(GPIO.BCM); print('GPIO OK')"

# Проверка подтягивающих резисторов
grep -i gpio /boot/config.txt
```

### Проблемы с сервисом
```bash
# Проверка статуса
sudo systemctl status lcd-game

# Просмотр логов
sudo journalctl -u lcd-game -f

# Перезапуск сервиса
sudo systemctl restart lcd-game
```

### Проблемы с поворотом экрана
```bash
# Проверка текущего поворота
grep display_rotate /boot/config.txt

# Сброс поворота
sudo /opt/lcd_game_driver/rotate_display.sh 0

# Проверка калибровки
ls -la /etc/X11/xorg.conf.d/99-calibration.conf
```

## 📞 Поддержка

### Полезные команды
```bash
# Информация о системе
cat /proc/cpuinfo | grep Model
cat /proc/device-tree/model

# Версия Python
python3 --version

# Установленные пакеты
pip3 list | grep -E "(Pillow|RPi|spidev|PyMouse)"

# Свободное место
df -h /opt/lcd_game_driver
```

### Логи и отладка
```bash
# Системные логи
sudo dmesg | tail -20

# Логи сервиса
sudo journalctl -u lcd-game --since "5 minutes ago"

# Логи установки
sudo cat /var/log/lcd_game/install.log
```

## 🎉 Готово!

После выполнения всех шагов у вас будет:

✅ **Полностью настроенная система** с LCD дисплеем  
✅ **Автоматический запуск** при загрузке  
✅ **Управление поворотом** экрана  
✅ **Эмулятор мыши** для управления  
✅ **Система тестирования** для диагностики  
✅ **Резервное копирование** конфигурации  

**Наслаждайтесь использованием CM4 LCD Game Driver!** 🎮