#!/usr/bin/env python3
"""
Простой тест дисплея для Raspberry Pi CM4 с LCD
Запускает базовое изображение на экране
"""

import time
from lcd_game import LCDGame
from config import COLORS

def simple_display_test():
    """Простой тест отображения"""
    try:
        print("Инициализация LCD дисплея...")

        # Создаем экземпляр дисплея
        lcd = LCDGame()
        print("✓ LCD дисплей инициализирован")

        # Очистка экрана
        print("Очистка экрана...")
        lcd.clear(COLORS['BLACK'])
        print("✓ Экран очищен")

        # Отображение приветственного текста
        print("Отображение текста...")
        lcd.draw_text("CM4 LCD Test", 40, 50, COLORS['WHITE'], 16)
        lcd.draw_text("SHIWA NETWORK", 30, 80, COLORS['GREEN'], 14)
        lcd.draw_text("Grand Mini", 50, 110, COLORS['BLUE'], 14)
        print("✓ Текст отображен")

        # Рисование простой геометрии
        print("Рисование фигур...")
        lcd.draw_rect(50, 140, 100, 40, COLORS['RED'], fill=True)
        lcd.draw_circle(120, 200, 25, COLORS['YELLOW'], fill=True)
        print("✓ Фигуры нарисованы")

        # Обновление дисплея
        print("Обновление дисплея...")
        lcd.update()
        print("✓ Дисплей обновлен")

        print("\n🎉 Тест завершен успешно!")
        print("Изображение должно отображаться на LCD экране")
        print("Нажмите Ctrl+C для выхода")

        # Ждем 5 секунд, затем мигаем подсветкой
        time.sleep(5)

        print("Тест подсветки...")
        for i in range(3):
            lcd.set_backlight(False)
            time.sleep(0.5)
            lcd.set_backlight(True)
            time.sleep(0.5)

        print("Тест завершен. Дисплей работает корректно!")

    except KeyboardInterrupt:
        print("\nТест прерван пользователем")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        print("Проверьте:")
        print("1. Правильность подключения дисплея")
        print("2. Включен ли SPI в raspi-config")
        print("3. Установлены ли зависимости: pip3 install -r requirements.txt")
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
    print("ПРОСТОЙ ТЕСТ LCD ДИСПЛЕЯ")
    print("Для Raspberry Pi CM4")
    print("=" * 50)
    simple_display_test()
