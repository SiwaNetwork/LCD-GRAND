#!/usr/bin/env python3
"""
Тест кнопок для 1.54 inch LCD GAME дисплея
Проверяет работу всех кнопок согласно схеме подключения
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lcd_game import LCDGame
import time

def test_buttons():
    """Тестирование всех кнопок"""
    try:
        print("Запуск теста кнопок...")
        print("Нажимайте кнопки для проверки их работы")
        print("Нажмите Ctrl+C для выхода")
        
        # Создание экземпляра дисплея
        lcd = LCDGame()
        
        # Очистка экрана
        lcd.clear()
        
        # Отображение инструкций
        lcd.draw_text("Button Test", 80, 20, color=(255, 255, 255), font_size=16)
        lcd.draw_text("Press buttons to test", 60, 50, color=(255, 255, 0))
        lcd.update()
        
        # Словарь для отслеживания состояния кнопок
        button_states = {}
        for button_name in lcd.buttons.button_states.keys():
            button_states[button_name] = False
        
        # Основной цикл тестирования
        while True:
            # Проверка каждой кнопки
            for button_name in lcd.buttons.button_states.keys():
                is_pressed = lcd.buttons.is_pressed(button_name)
                is_held = lcd.buttons.is_held(button_name)
                
                # Если кнопка была нажата
                if is_pressed:
                    print(f"Кнопка {button_name} нажата!")
                    button_states[button_name] = True
                
                # Если кнопка отпущена
                elif button_states[button_name] and not is_held:
                    button_states[button_name] = False
            
            # Обновление отображения
            lcd.clear()
            lcd.draw_text("Button Test", 80, 20, color=(255, 255, 255), font_size=16)
            
            # Отображение состояния кнопок
            y_pos = 50
            for i, (button_name, is_pressed) in enumerate(button_states.items()):
                color = (0, 255, 0) if is_pressed else (255, 255, 255)
                lcd.draw_text(f"{button_name}: {'ON' if is_pressed else 'OFF'}", 
                            10, y_pos, color=color, font_size=12)
                y_pos += 15
                
                # Переход на новую строку каждые 3 кнопки
                if (i + 1) % 3 == 0:
                    y_pos += 5
            
            lcd.update()
            time.sleep(0.1)  # Небольшая задержка
            
    except KeyboardInterrupt:
        print("\nЗавершение теста кнопок...")
        lcd.cleanup()
    except Exception as e:
        print(f"Ошибка: {e}")
        lcd.cleanup()

if __name__ == "__main__":
    test_buttons()