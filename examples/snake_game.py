#!/usr/bin/env python3
"""
Пример игры "Змейка" для 1.54 inch LCD GAME дисплея
"""

import random
import time
from lcd_game import LCDGame, GameEngine
from config import COLORS

class SnakeGame(GameEngine):
    """
    Классическая игра "Змейка"
    """
    
    def __init__(self, lcd):
        super().__init__(lcd)
        self.fps = 10  # Скорость игры
        self.reset_game()
    
    def reset_game(self):
        """Сброс игры"""
        # Инициализация змейки
        self.snake = [(120, 120)]  # Начальная позиция
        self.direction = (1, 0)  # Направление движения
        self.food = self.generate_food()
        self.score = 0
        self.game_over = False
        
    def generate_food(self):
        """Генерация еды"""
        while True:
            x = random.randint(0, 23) * 10  # 240 / 10 = 24
            y = random.randint(0, 23) * 10
            if (x, y) not in self.snake:
                return (x, y)
    
    def handle_input(self):
        """Обработка ввода (можно расширить для кнопок)"""
        # Здесь можно добавить обработку кнопок
        # Пока используем случайное изменение направления
        if random.random() < 0.1:  # 10% шанс изменения направления
            directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            new_direction = random.choice(directions)
            # Проверка, что не идем в противоположном направлении
            if (new_direction[0] != -self.direction[0] or 
                new_direction[1] != -self.direction[1]):
                self.direction = new_direction
    
    def update(self, delta_time):
        """Обновление игровой логики"""
        if self.game_over:
            return
        
        # Обработка ввода
        self.handle_input()
        
        # Движение змейки
        head = self.snake[0]
        new_head = (head[0] + self.direction[0] * 10, 
                   head[1] + self.direction[1] * 10)
        
        # Проверка границ
        if (new_head[0] < 0 or new_head[0] >= 240 or 
            new_head[1] < 0 or new_head[1] >= 240):
            self.game_over = True
            return
        
        # Проверка столкновения с собой
        if new_head in self.snake:
            self.game_over = True
            return
        
        # Добавление новой головы
        self.snake.insert(0, new_head)
        
        # Проверка еды
        if new_head == self.food:
            self.score += 10
            self.food = self.generate_food()
            # Увеличение скорости
            self.fps = min(20, 10 + self.score // 50)
        else:
            # Удаление хвоста
            self.snake.pop()
    
    def render(self):
        """Отрисовка игры"""
        # Очистка экрана
        self.lcd.clear()
        
        if self.game_over:
            # Экран окончания игры
            self.lcd.draw_text("GAME OVER", 70, 80, COLORS['RED'], 16)
            self.lcd.draw_text(f"Score: {self.score}", 90, 110, COLORS['WHITE'], 12)
            self.lcd.draw_text("Press any key", 70, 140, COLORS['YELLOW'], 10)
        else:
            # Отрисовка змейки
            for i, segment in enumerate(self.snake):
                if i == 0:  # Голова
                    self.lcd.draw_rect(segment[0], segment[1], 10, 10, 
                                     COLORS['GREEN'], fill=True)
                else:  # Тело
                    self.lcd.draw_rect(segment[0], segment[1], 10, 10, 
                                     COLORS['DARK_GRAY'], fill=True)
            
            # Отрисовка еды
            self.lcd.draw_rect(self.food[0], self.food[1], 10, 10, 
                             COLORS['RED'], fill=True)
            
            # Отрисовка счета
            self.lcd.draw_text(f"Score: {self.score}", 10, 10, COLORS['WHITE'], 10)
        
        # Обновление дисплея
        self.lcd.update()


def main():
    """Основная функция"""
    try:
        print("Запуск игры 'Змейка'...")
        lcd = LCDGame()
        game = SnakeGame(lcd)
        
        print("Игра запущена! Нажмите Ctrl+C для выхода.")
        game.start()
        
    except KeyboardInterrupt:
        print("\nЗавершение игры...")
        lcd.cleanup()
    except Exception as e:
        print(f"Ошибка: {e}")
        lcd.cleanup()


if __name__ == "__main__":
    main()