#!/usr/bin/env python3
"""
Тест отображения изображения на LCD дисплее
Создает и показывает простое изображение
"""

import time
from PIL import Image, ImageDraw, ImageFont
from lcd_game import LCDGame
from config import COLORS

def create_test_image():
    """Создание тестового изображения"""
    # Создаем новое изображение 240x240
    img = Image.new('RGB', (240, 240), color=COLORS['BLACK'])
    draw = ImageDraw.Draw(img)

    # Рисуем градиентный фон
    for y in range(240):
        r = int(255 * y / 240)
        g = int(128 * (240 - y) / 240)
        b = int(255 * y / 240)
        draw.line([(0, y), (240, y)], fill=(r, g, b))

    # Рисуем текст
    try:
        font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
        font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()

    # Текст в центре
    draw.text((20, 50), "IMAGE TEST", fill=COLORS['WHITE'], font=font_large)
    draw.text((30, 90), "Raspberry Pi CM4", fill=COLORS['GREEN'], font=font_medium)
    draw.text((50, 120), "LCD Display", fill=COLORS['BLUE'], font=font_medium)

    # Рисуем геометрические фигуры
    draw.rectangle([20, 150, 100, 190], fill=COLORS['RED'], outline=COLORS['WHITE'])
    draw.ellipse([140, 160, 200, 220], fill=COLORS['YELLOW'], outline=COLORS['BLACK'])

    # Рисуем сетку
    for i in range(0, 241, 20):
        draw.line([(i, 0), (i, 240)], fill=COLORS['GRAY'], width=1)
        draw.line([(0, i), (240, i)], fill=COLORS['GRAY'], width=1)

    return img

def display_image_test():
    """Тест отображения изображения"""
    try:
        print("Создание тестового изображения...")

        # Создаем изображение
        test_image = create_test_image()
        print("✓ Изображение создано")

        print("Инициализация LCD дисплея...")
        lcd = LCDGame()
        print("✓ LCD дисплей инициализирован")

        print("Отображение изображения...")
        # Устанавливаем изображение в буфер дисплея
        lcd.set_buffer(test_image)

        # Обновляем дисплей
        lcd.update()
        print("✓ Изображение отображено")

        print("\n🎉 Изображение успешно отображено!")
        print("На экране должно быть видно:")
        print("- Градиентный фон")
        print("- Текст 'IMAGE TEST'")
        print("- Геометрические фигуры")
        print("- Координатная сетка")

        # Анимация - мигаем подсветкой
        print("\nТест подсветки...")
        for i in range(3):
            time.sleep(1)
            lcd.set_backlight(False)
            time.sleep(0.5)
            lcd.set_backlight(True)

        print("Тест завершен!")
        input("Нажмите Enter для выхода...")

    except KeyboardInterrupt:
        print("\nТест прерван пользователем")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        print("Возможные причины:")
        print("1. Дисплей не подключен")
        print("2. SPI не включен в raspi-config")
        print("3. Неправильное подключение GPIO")
        print("4. Не установлены зависимости")
    finally:
        try:
            if 'lcd' in locals():
                print("Очистка ресурсов...")
                lcd.cleanup()
                print("✓ Ресурсы очищены")
        except:
            pass

if __name__ == "__main__":
    print("=" * 50)
    print("ТЕСТ ОТОБРАЖЕНИЯ ИЗОБРАЖЕНИЯ")
    print("Для Raspberry Pi CM4 с LCD дисплеем")
    print("=" * 50)
    display_image_test()
