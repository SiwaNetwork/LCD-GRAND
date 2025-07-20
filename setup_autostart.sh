#!/bin/bash
"""
Скрипт настройки автозапуска системы CM4
"""

# Путь к проекту
PROJECT_DIR="/workspace"
START_SCRIPT="$PROJECT_DIR/start_system.sh"

echo "Настройка автозапуска системы SHIWA NETWORK Grand Mini..."

# Проверка существования скрипта запуска
if [ ! -f "$START_SCRIPT" ]; then
    echo "Ошибка: Скрипт запуска не найден"
    exit 1
fi

# Создание systemd сервиса
SERVICE_FILE="/etc/systemd/system/shiwa-network.service"

echo "Создание systemd сервиса..."

cat > "$SERVICE_FILE" << EOF
[Unit]
Description=SHIWA NETWORK Grand Mini System
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=$PROJECT_DIR
ExecStart=$START_SCRIPT
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Установка прав на сервис
chmod 644 "$SERVICE_FILE"

# Перезагрузка systemd
systemctl daemon-reload

# Включение автозапуска
systemctl enable shiwa-network.service

echo "Автозапуск настроен!"
echo "Команды управления:"
echo "  Запуск: sudo systemctl start shiwa-network"
echo "  Остановка: sudo systemctl stop shiwa-network"
echo "  Статус: sudo systemctl status shiwa-network"
echo "  Отключение автозапуска: sudo systemctl disable shiwa-network"