#!/usr/bin/env python3
"""
Тестовый скрипт для проверки работы системы CM4
"""

import time
import sys
from lcd_game import LCDGame
from boot_splash import BootSplash
from desktop import Desktop

def test_lcd():
    """Тест LCD дисплея"""
    print("Тестирование LCD дисплея...")
    try:
        lcd = LCDGame()
        print("✓ LCD дисплей инициализирован")
        
        # Тест очистки
        lcd.clear()
        lcd.update()
        print("✓ Очистка экрана")
        
        # Тест отрисовки текста
        lcd.draw_text("LCD Test", 10, 10, color=(255, 255, 255))
        lcd.update()
        print("✓ Отрисовка текста")
        
        # Тест геометрических фигур
        lcd.draw_rect(50, 50, 100, 50, color=(255, 0, 0), fill=True)
        lcd.draw_circle(150, 150, 30, color=(0, 255, 0), fill=True)
        lcd.update()
        print("✓ Отрисовка фигур")
        
        time.sleep(2)
        lcd.cleanup()
        return True
        
    except Exception as e:
        print(f"✗ Ошибка LCD: {e}")
        return False

def test_buttons():
    """Тест кнопок"""
    print("Тестирование кнопок...")
    try:
        lcd = LCDGame()
        
        # Очистка экрана
        lcd.clear()
        lcd.draw_text("Button Test", 10, 10, color=(255, 255, 255))
        lcd.draw_text("Press any button", 10, 30, color=(200, 200, 200))
        lcd.update()
        
        # Ожидание нажатия кнопки
        start_time = time.time()
        while time.time() - start_time < 10:  # 10 секунд на тест
            for button_name in ['A', 'B', 'UP', 'DOWN', 'LEFT', 'RIGHT', 'START', 'SELECT']:
                if lcd.buttons.is_pressed(button_name):
                    print(f"✓ Кнопка {button_name} работает")
                    lcd.draw_text(f"Pressed: {button_name}", 10, 60, color=(0, 255, 0))
                    lcd.update()
                    time.sleep(0.5)
            
            time.sleep(0.1)
        
        lcd.cleanup()
        return True
        
    except Exception as e:
        print(f"✗ Ошибка кнопок: {e}")
        return False

def test_splash():
    """Тест заставки"""
    print("Тестирование заставки...")
    try:
        lcd = LCDGame()
        splash = BootSplash(lcd)
        
        # Быстрый тест заставки
        splash.show_logo_animation()
        time.sleep(1)
        
        splash.show_text_animation()
        time.sleep(1)
        
        splash.show_loading_animation()
        time.sleep(1)
        
        print("✓ Заставка работает")
        lcd.cleanup()
        return True
        
    except Exception as e:
        print(f"✗ Ошибка заставки: {e}")
        return False

def test_desktop():
    """Тест рабочего стола"""
    print("Тестирование рабочего стола...")
    try:
        lcd = LCDGame()
        desktop = Desktop(lcd)
        
        # Тест отрисовки главного экрана
        desktop.draw_main_screen()
        lcd.update()
        print("✓ Главный экран отрисован")
        
        # Тест других экранов
        desktop.draw_system_info_screen()
        lcd.update()
        print("✓ Экран системной информации")
        
        desktop.draw_games_screen()
        lcd.update()
        print("✓ Экран игр")
        
        time.sleep(2)
        lcd.cleanup()
        return True
        
    except Exception as e:
        print(f"✗ Ошибка рабочего стола: {e}")
        return False

def main():
    """Главная функция тестирования"""
    print("=" * 50)
    print("Тестирование системы SHIWA NETWORK Grand Mini")
    print("=" * 50)
    
    tests = [
        ("LCD дисплей", test_lcd),
        ("Кнопки", test_buttons),
        ("Заставка", test_splash),
        ("Рабочий стол", test_desktop)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n--- Тест: {test_name} ---")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ Критическая ошибка в тесте {test_name}: {e}")
            results.append((test_name, False))
    
    # Вывод результатов
    print("\n" + "=" * 50)
    print("РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ")
    print("=" * 50)
    
    passed = 0
    for test_name, result in results:
        status = "✓ ПРОЙДЕН" if result else "✗ ПРОВАЛЕН"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nВсего тестов: {len(results)}")
    print(f"Пройдено: {passed}")
    print(f"Провалено: {len(results) - passed}")
    
    if passed == len(results):
        print("\n🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ! Система готова к работе.")
        print("\nДля запуска системы выполните:")
        print("sudo python3 main.py")
    else:
        print("\n⚠️ Некоторые тесты провалены. Проверьте подключение и настройки.")
    
    return passed == len(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)