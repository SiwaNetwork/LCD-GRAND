#!/bin/bash
"""
Скрипт автозапуска системы CM4 с LCD дисплеем
"""

# Путь к проекту
PROJECT_DIR="/workspace"
PYTHON_SCRIPT="$PROJECT_DIR/main.py"

# Проверка существования файла
if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo "Ошибка: Файл $PYTHON_SCRIPT не найден"
    exit 1
fi

# Переход в директорию проекта
cd "$PROJECT_DIR"

# Проверка зависимостей
echo "Проверка зависимостей..."
python3 -c "import psutil, RPi.GPIO, spidev, PIL" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Установка зависимостей..."
    pip3 install -r requirements.txt
fi

# Включение SPI интерфейса (если не включен)
if ! grep -q "dtparam=spi=on" /boot/config.txt; then
    echo "Включение SPI интерфейса..."
    echo "dtparam=spi=on" | sudo tee -a /boot/config.txt
    echo "Требуется перезагрузка для применения изменений"
fi

# Запуск системы
echo "Запуск системы SHIWA NETWORK Grand Mini..."
sudo python3 "$PYTHON_SCRIPT"