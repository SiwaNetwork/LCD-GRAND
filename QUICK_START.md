# Быстрый старт - 1.54 inch LCD GAME

## Подключение согласно схеме

### Основные пины дисплея
- **RST** → Pin 13 (GPIO 27)
- **DC** → Pin 15 (GPIO 22)  
- **CS** → Pin 24 (GPIO 8)
- **BL** → Pin 12 (GPIO 18)
- **MOSI** → Pin 19 (GPIO 10)
- **MISO** → Pin 21 (GPIO 9)
- **SCK** → Pin 23 (GPIO 11)
- **3.3V** → Pin 1 или 17
- **GND** → Любой GND пин

### Кнопки управления
- **A** → Pin 40 (GPIO 21)
- **B** → Pin 38 (GPIO 20)
- **UP** → Pin 36 (GPIO 16)
- **DOWN** → Pin 29 (GPIO 5)
- **LEFT** → Pin 31 (GPIO 6)
- **RIGHT** → Pin 33 (GPIO 13)
- **START** → Pin 35 (GPIO 19)
- **SELECT** → Pin 37 (GPIO 26)
- **MENU** → Pin 11 (GPIO 17)

## Установка

1. **Включите SPI:**
   ```bash
   sudo raspi-config
   # Interface Options → SPI → Enable
   ```

2. **Установите зависимости:**
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-dev
   pip3 install -r requirements.txt
   ```

3. **Запустите установку:**
   ```bash
   sudo ./install.sh
   ```

## Тестирование

1. **Тест дисплея:**
   ```bash
   python3 lcd_game.py
   ```

2. **Тест кнопок:**
   ```bash
   python3 examples/button_test.py
   ```

3. **Простая игра:**
   ```bash
   python3 examples/simple_game.py
   ```

## Управление в игре

- **UP/DOWN/LEFT/RIGHT** - Движение
- **A/B** - Действия
- **START** - Пауза/Возобновление
- **SELECT** - Перезапуск
- **MENU** - Меню

## Устранение проблем

### Дисплей не работает
- Проверьте питание (3.3V и GND)
- Убедитесь, что SPI включен
- Проверьте подключение RST, DC, CS

### Кнопки не реагируют  
- Проверьте подключение к соответствующим GPIO
- Убедитесь в правильной нумерации (BCM)
- Проверьте подтягивающие резисторы

### Медленная работа
- Уменьшите SPI_SPEED в config.py
- Проверьте качество соединений

## Следующие шаги

1. Изучите `config.py` для настройки
2. Посмотрите примеры в папке `examples/`
3. Создайте свою игру, наследуясь от `GameEngine`
4. Обратитесь к `docs/PINOUT_GUIDE.md` для подробной схемы