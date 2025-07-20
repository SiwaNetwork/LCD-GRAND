#!/usr/bin/env python3
"""
Пример простой игры для 1.54 inch LCD GAME дисплея
Демонстрирует использование кнопок согласно схеме подключения
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lcd_game import LCDGame, GameEngine
import time

class SimpleGame(GameEngine):
    """
    Простая игра с управлением кнопками
    """
    
    def __init__(self, lcd):
        super().__init__(lcd)
        self.player_x = 120
        self.player_y = 120
        self.player_size = 10
        self.score = 0
        self.game_state = "playing"  # playing, paused, game_over
        
    def handle_input(self):
        """Обработка ввода от кнопок"""
        # Движение игрока
        if self.lcd.buttons.is_held('UP'):
            self.player_y = max(self.player_size, self.player_y - 3)
        if self.lcd.buttons.is_held('DOWN'):
            self.player_y = min(self.lcd.height - self.player_size, self.player_y + 3)
        if self.lcd.buttons.is_held('LEFT'):
            self.player_x = max(self.player_size, self.player_x - 3)
        if self.lcd.buttons.is_held('RIGHT'):
            self.player_x = min(self.lcd.width - self.player_size, self.player_x + 3)
        
        # Действия кнопок
        if self.lcd.buttons.is_pressed('A'):
            self.score += 10
            print(f"Кнопка A нажата! Счет: {self.score}")
        
        if self.lcd.buttons.is_pressed('B'):
            self.score += 5
            print(f"Кнопка B нажата! Счет: {self.score}")
        
        if self.lcd.buttons.is_pressed('START'):
            if self.game_state == "playing":
                self.game_state = "paused"
                print("Игра приостановлена")
            elif self.game_state == "paused":
                self.game_state = "playing"
                print("Игра возобновлена")
        
        if self.lcd.buttons.is_pressed('SELECT'):
            self.score = 0
            self.player_x = 120
            self.player_y = 120
            self.game_state = "playing"
            print("Игра перезапущена")
    
    def update(self, delta_time):
        """Обновление игровой логики"""
        if self.game_state != "playing":
            return
        
        # Простая логика игры
        self.score += int(delta_time * 10)  # Увеличение счета со временем
    
    def render(self):
        """Отрисовка игры"""
        # Очистка экрана
        self.lcd.clear(color=(0, 0, 0))
        
        if self.game_state == "playing":
            # Рисование игрока
            self.lcd.draw_circle(self.player_x, self.player_y, self.player_size, 
                               color=(0, 255, 0), fill=True)
            
            # Рисование границ
            self.lcd.draw_rect(0, 0, self.lcd.width, self.lcd.height, 
                             color=(255, 255, 255), fill=False)
            
            # Отображение счета
            self.lcd.draw_text(f"Score: {self.score}", 10, 10, color=(255, 255, 255))
            
            # Отображение инструкций
            self.lcd.draw_text("A/B: +points", 10, 30, color=(255, 255, 0), font_size=10)
            self.lcd.draw_text("START: pause", 10, 45, color=(255, 255, 0), font_size=10)
            self.lcd.draw_text("SELECT: reset", 10, 60, color=(255, 255, 0), font_size=10)
            
        elif self.game_state == "paused":
            self.lcd.draw_text("PAUSED", 100, 100, color=(255, 255, 0), font_size=20)
            self.lcd.draw_text("Press START to resume", 60, 130, color=(255, 255, 255))
        
        # Обновление дисплея
        self.lcd.update()

def main():
    """Основная функция"""
    try:
        print("Запуск простой игры...")
        print("Используйте кнопки для управления:")
        print("- UP/DOWN/LEFT/RIGHT: Движение")
        print("- A/B: Добавить очки")
        print("- START: Пауза/Возобновление")
        print("- SELECT: Перезапуск игры")
        
        # Создание экземпляра дисплея
        lcd = LCDGame()
        
        # Создание и запуск игры
        game = SimpleGame(lcd)
        game.start()
        
    except KeyboardInterrupt:
        print("\nЗавершение игры...")
        lcd.cleanup()
    except Exception as e:
        print(f"Ошибка: {e}")
        lcd.cleanup()

if __name__ == "__main__":
    main()