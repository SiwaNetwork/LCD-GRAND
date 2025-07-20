#!/usr/bin/env python3
"""
Заставка включения для CM4 с LCD дисплеем
Анимация с надписью SHIWA NETWORK Grand Mini
"""

import time
import math
from lcd_game import LCDGame
from config import *

class BootSplash:
    """
    Класс для отображения заставки включения
    """
    
    def __init__(self, lcd):
        """
        Инициализация заставки
        
        Args:
            lcd: Экземпляр LCDGame
        """
        self.lcd = lcd
        self.width = DISPLAY_WIDTH
        self.height = DISPLAY_HEIGHT
        
    def show_logo_animation(self):
        """Анимация логотипа с появлением"""
        # Очистка экрана
        self.lcd.clear()
        
        # Анимация появления логотипа
        for i in range(0, 121, 3):
            # Рисуем круг логотипа
            self.lcd.draw_circle(
                self.width // 2, 
                self.height // 2 - 20, 
                i, 
                color=(0, 150, 255), 
                fill=False
            )
            self.lcd.update()
            time.sleep(0.02)
        
        # Заполнение логотипа
        for i in range(0, 121, 5):
            self.lcd.draw_circle(
                self.width // 2, 
                self.height // 2 - 20, 
                120 - i, 
                color=(0, 150, 255), 
                fill=True
            )
            self.lcd.update()
            time.sleep(0.01)
    
    def show_text_animation(self):
        """Анимация появления текста"""
        # Основной текст
        main_text = "SHIWA NETWORK"
        sub_text = "Grand Mini"
        
        # Анимация появления основного текста
        for i in range(len(main_text) + 1):
            self.lcd.clear()
            self.lcd.draw_circle(
                self.width // 2, 
                self.height // 2 - 20, 
                120, 
                color=(0, 150, 255), 
                fill=True
            )
            self.lcd.draw_text(
                main_text[:i], 
                self.width // 2 - 60, 
                self.height // 2 - 10, 
                color=(255, 255, 255), 
                font_size=16
            )
            self.lcd.update()
            time.sleep(0.1)
        
        # Анимация появления подзаголовка
        for i in range(len(sub_text) + 1):
            self.lcd.draw_text(
                sub_text[:i], 
                self.width // 2 - 40, 
                self.height // 2 + 20, 
                color=(200, 200, 200), 
                font_size=14
            )
            self.lcd.update()
            time.sleep(0.08)
    
    def show_loading_animation(self):
        """Анимация загрузки"""
        # Прогресс-бар
        bar_width = 200
        bar_height = 8
        bar_x = (self.width - bar_width) // 2
        bar_y = self.height - 40
        
        for progress in range(0, 101, 2):
            # Очистка области прогресс-бара
            self.lcd.draw_rect(
                bar_x - 2, 
                bar_y - 2, 
                bar_width + 4, 
                bar_height + 4, 
                color=(50, 50, 50), 
                fill=True
            )
            
            # Рамка прогресс-бара
            self.lcd.draw_rect(
                bar_x, 
                bar_y, 
                bar_width, 
                bar_height, 
                color=(100, 100, 100), 
                fill=False
            )
            
            # Заполнение прогресс-бара
            fill_width = int((progress / 100) * bar_width)
            if fill_width > 0:
                self.lcd.draw_rect(
                    bar_x, 
                    bar_y, 
                    fill_width, 
                    bar_height, 
                    color=(0, 255, 0), 
                    fill=True
                )
            
            # Текст прогресса
            self.lcd.draw_text(
                f"Loading... {progress}%", 
                self.width // 2 - 50, 
                bar_y - 20, 
                color=(255, 255, 255), 
                font_size=12
            )
            
            self.lcd.update()
            time.sleep(0.05)
    
    def show_pulse_animation(self):
        """Пульсирующая анимация"""
        for _ in range(3):
            # Увеличение яркости
            for i in range(0, 255, 10):
                # Создаем эффект свечения вокруг логотипа
                glow_radius = 130 + int(i / 25)
                self.lcd.draw_circle(
                    self.width // 2, 
                    self.height // 2 - 20, 
                    glow_radius, 
                    color=(0, i, 255), 
                    fill=False
                )
                self.lcd.update()
                time.sleep(0.01)
            
            # Уменьшение яркости
            for i in range(255, 0, -10):
                glow_radius = 130 + int(i / 25)
                self.lcd.draw_circle(
                    self.width // 2, 
                    self.height // 2 - 20, 
                    glow_radius, 
                    color=(0, i, 255), 
                    fill=False
                )
                self.lcd.update()
                time.sleep(0.01)
    
    def show_complete_animation(self):
        """Финальная анимация"""
        # Эффект "готово"
        for i in range(5):
            self.lcd.draw_text(
                "READY", 
                self.width // 2 - 30, 
                self.height - 60, 
                color=(0, 255, 0), 
                font_size=14
            )
            self.lcd.update()
            time.sleep(0.3)
            
            self.lcd.draw_text(
                "READY", 
                self.width // 2 - 30, 
                self.height - 60, 
                color=(0, 0, 0), 
                font_size=14
            )
            self.lcd.update()
            time.sleep(0.3)
    
    def run(self):
        """Запуск полной анимации заставки"""
        try:
            print("Запуск заставки включения...")
            
            # 1. Анимация логотипа
            self.show_logo_animation()
            time.sleep(0.5)
            
            # 2. Анимация текста
            self.show_text_animation()
            time.sleep(0.5)
            
            # 3. Пульсирующая анимация
            self.show_pulse_animation()
            
            # 4. Анимация загрузки
            self.show_loading_animation()
            
            # 5. Финальная анимация
            self.show_complete_animation()
            
            # Пауза перед переходом к рабочему столу
            time.sleep(1.0)
            
            print("Заставка завершена")
            
        except Exception as e:
            print(f"Ошибка в заставке: {e}")

if __name__ == "__main__":
    # Тест заставки
    lcd = LCDGame()
    splash = BootSplash(lcd)
    splash.run()
    lcd.cleanup()