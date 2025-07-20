#!/usr/bin/env python3
"""
Улучшенный тестовый скрипт для проверки работы системы CM4
Включает тестирование системной интеграции и новых функций
"""

import time
import sys
import os
import subprocess
from lcd_game import LCDGame
from boot_splash import BootSplash
from desktop import Desktop

def test_system_integration():
    """Тест системной интеграции"""
    print("Тестирование системной интеграции...")
    
    tests = []
    
    # Проверка SPI интерфейса
    try:
        if os.path.exists('/dev/spidev0.0'):
            print("✓ SPI устройство найдено")
            tests.append(True)
        else:
            print("✗ SPI устройство не найдено")
            tests.append(False)
    except Exception as e:
        print(f"✗ Ошибка проверки SPI: {e}")
        tests.append(False)
    
    # Проверка GPIO
    try:
        import RPi.GPIO as GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.cleanup()
        print("✓ GPIO доступен")
        tests.append(True)
    except Exception as e:
        print(f"✗ Ошибка GPIO: {e}")
        tests.append(False)
    
    # Проверка config.txt
    try:
        with open('/boot/config.txt', 'r') as f:
            config_content = f.read()
        
        if 'dtparam=spi=on' in config_content:
            print("✓ SPI настроен в config.txt")
            tests.append(True)
        else:
            print("⚠ SPI не настроен в config.txt")
            tests.append(False)
        
        if 'gpio=' in config_content and '=pu' in config_content:
            print("✓ GPIO подтягивающие резисторы настроены")
            tests.append(True)
        else:
            print("⚠ GPIO подтягивающие резисторы не настроены")
            tests.append(False)
            
    except Exception as e:
        print(f"✗ Ошибка проверки config.txt: {e}")
        tests.append(False)
    
    # Проверка поворота экрана
    try:
        rotation_found = False
        for line in config_content.split('\n'):
            if line.strip().startswith('display_rotate='):
                angle = int(line.split('=')[1].strip())
                print(f"✓ Текущий поворот экрана: {angle}°")
                rotation_found = True
                tests.append(True)
                break
        
        if not rotation_found:
            print("⚠ Поворот экрана не настроен")
            tests.append(False)
            
    except Exception as e:
        print(f"✗ Ошибка проверки поворота: {e}")
        tests.append(False)
    
    # Проверка калибровки сенсора
    try:
        calibration_file = '/etc/X11/xorg.conf.d/99-calibration.conf'
        if os.path.exists(calibration_file):
            print("✓ Файл калибровки сенсора найден")
            tests.append(True)
        else:
            print("⚠ Файл калибровки сенсора не найден")
            tests.append(False)
    except Exception as e:
        print(f"✗ Ошибка проверки калибровки: {e}")
        tests.append(False)
    
    # Проверка systemd сервиса
    try:
        result = subprocess.run(['systemctl', 'is-active', 'lcd-game'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ LCD Game сервис активен")
            tests.append(True)
        else:
            print("⚠ LCD Game сервис не активен")
            tests.append(False)
    except Exception as e:
        print(f"✗ Ошибка проверки сервиса: {e}")
        tests.append(False)
    
    # Проверка PyMouse
    try:
        import pymouse
        print("✓ PyMouse установлен")
        tests.append(True)
    except ImportError:
        print("✗ PyMouse не установлен")
        tests.append(False)
    
    return all(tests)

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
        
        # Тест поворота
        lcd.set_rotation(90)
        lcd.clear()
        lcd.draw_text("Rotated 90°", 10, 10, color=(255, 255, 255))
        lcd.update()
        print("✓ Поворот дисплея")
        
        # Возврат к исходному повороту
        lcd.set_rotation(0)
        
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
        lcd.draw_text("Timeout: 10s", 10, 50, color=(150, 150, 150))
        lcd.update()
        
        # Ожидание нажатия кнопки
        start_time = time.time()
        pressed_buttons = []
        
        while time.time() - start_time < 10:  # 10 секунд на тест
            for button_name in ['A', 'B', 'UP', 'DOWN', 'LEFT', 'RIGHT', 'START', 'SELECT']:
                if lcd.buttons.is_pressed(button_name):
                    if button_name not in pressed_buttons:
                        pressed_buttons.append(button_name)
                        print(f"✓ Кнопка {button_name} работает")
                        lcd.draw_text(f"Pressed: {button_name}", 10, 80 + len(pressed_buttons) * 15, 
                                    color=(0, 255, 0))
                        lcd.update()
            
            time.sleep(0.1)
        
        if pressed_buttons:
            print(f"✓ Найдено работающих кнопок: {len(pressed_buttons)}")
            print(f"  Работающие кнопки: {', '.join(pressed_buttons)}")
        else:
            print("⚠ Ни одна кнопка не была нажата")
        
        lcd.cleanup()
        return len(pressed_buttons) > 0
        
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
        time.sleep(0.5)
        
        splash.show_text_animation()
        time.sleep(0.5)
        
        splash.show_loading_animation()
        time.sleep(0.5)
        
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
        
        desktop.draw_settings_screen()
        lcd.update()
        print("✓ Экран настроек")
        
        time.sleep(2)
        lcd.cleanup()
        return True
        
    except Exception as e:
        print(f"✗ Ошибка рабочего стола: {e}")
        return False

def test_mouse_emulator():
    """Тест эмулятора мыши"""
    print("Тестирование эмулятора мыши...")
    try:
        # Проверка наличия файла эмулятора
        emulator_path = "/opt/lcd_game_driver/mouse_emulator.py"
        if os.path.exists(emulator_path):
            print("✓ Файл эмулятора мыши найден")
            
            # Проверка прав на выполнение
            if os.access(emulator_path, os.X_OK):
                print("✓ Файл эмулятора исполняемый")
                return True
            else:
                print("⚠ Файл эмулятора не исполняемый")
                return False
        else:
            print("✗ Файл эмулятора мыши не найден")
            return False
            
    except Exception as e:
        print(f"✗ Ошибка проверки эмулятора мыши: {e}")
        return False

def test_rotation_script():
    """Тест скрипта поворота экрана"""
    print("Тестирование скрипта поворота экрана...")
    try:
        rotation_script = "/opt/lcd_game_driver/rotate_display.sh"
        if os.path.exists(rotation_script):
            print("✓ Скрипт поворота экрана найден")
            
            # Проверка прав на выполнение
            if os.access(rotation_script, os.X_OK):
                print("✓ Скрипт поворота исполняемый")
                return True
            else:
                print("⚠ Скрипт поворота не исполняемый")
                return False
        else:
            print("✗ Скрипт поворота экрана не найден")
            return False
            
    except Exception as e:
        print(f"✗ Ошибка проверки скрипта поворота: {e}")
        return False

def test_backup_system():
    """Тест системы резервного копирования"""
    print("Тестирование системы резервного копирования...")
    try:
        backup_dir = "/opt/lcd_game_backup"
        if os.path.exists(backup_dir):
            print("✓ Директория резервного копирования найдена")
            
            # Проверка наличия резервных копий
            backups = [d for d in os.listdir(backup_dir) if os.path.isdir(os.path.join(backup_dir, d))]
            if backups:
                print(f"✓ Найдено резервных копий: {len(backups)}")
                return True
            else:
                print("⚠ Резервные копии не найдены")
                return False
        else:
            print("✗ Директория резервного копирования не найдена")
            return False
            
    except Exception as e:
        print(f"✗ Ошибка проверки резервного копирования: {e}")
        return False

def main():
    """Главная функция тестирования"""
    print("=" * 60)
    print("Улучшенное тестирование системы SHIWA NETWORK Grand Mini")
    print("=" * 60)
    
    tests = [
        ("Системная интеграция", test_system_integration),
        ("LCD дисплей", test_lcd),
        ("Кнопки", test_buttons),
        ("Заставка", test_splash),
        ("Рабочий стол", test_desktop),
        ("Эмулятор мыши", test_mouse_emulator),
        ("Скрипт поворота", test_rotation_script),
        ("Резервное копирование", test_backup_system)
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
    print("\n" + "=" * 60)
    print("РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ")
    print("=" * 60)
    
    passed = 0
    for test_name, result in results:
        status = "✓ ПРОЙДЕН" if result else "✗ ПРОВАЛЕН"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nВсего тестов: {len(results)}")
    print(f"Пройдено: {passed}")
    print(f"Провалено: {len(results) - passed}")
    
    # Рекомендации
    print("\n" + "=" * 60)
    print("РЕКОМЕНДАЦИИ")
    print("=" * 60)
    
    if passed == len(results):
        print("🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ! Система готова к работе.")
        print("\nДля запуска системы выполните:")
        print("sudo python3 main.py")
        print("\nДля управления сервисом:")
        print("sudo systemctl start lcd-game")
    else:
        print("⚠️ Некоторые тесты провалены. Рекомендации:")
        
        failed_tests = [name for name, result in results if not result]
        
        if "Системная интеграция" in failed_tests:
            print("- Запустите системную интеграцию: sudo python3 system_manager.py")
        
        if "LCD дисплей" in failed_tests:
            print("- Проверьте подключение дисплея и SPI настройки")
        
        if "Кнопки" in failed_tests:
            print("- Проверьте подключение кнопок и GPIO настройки")
        
        if "Эмулятор мыши" in failed_tests:
            print("- Переустановите PyMouse: pip3 install PyMouse")
        
        if "Скрипт поворота" in failed_tests:
            print("- Переустановите систему: sudo ./install_enhanced.sh")
        
        print("\nДля диагностики выполните:")
        print("sudo dmesg | grep -i spi")
        print("sudo dmesg | grep -i gpio")
        print("ls -la /dev/spidev*")
    
    return passed == len(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)