#!/usr/bin/env python3
"""
Демонстрация возможностей 1.54 inch LCD GAME дисплея
"""

import time
import math
from lcd_game import LCDGame
from config import COLORS

class LCDDemo:
    """
    Демонстрация возможностей LCD дисплея
    """
    
    def __init__(self):
        self.lcd = LCDGame()
        self.frame = 0
        
    def demo_text(self):
        """Демонстрация текста"""
        print("Демонстрация текста...")
        self.lcd.clear()
        
        # Разные размеры шрифтов
        self.lcd.draw_text("LCD Demo", 10, 10, COLORS['WHITE'], 20)
        self.lcd.draw_text("CM4 Ready!", 10, 40, COLORS['GREEN'], 16)
        self.lcd.draw_text("240x240 Display", 10, 70, COLORS['BLUE'], 12)
        self.lcd.draw_text("ST7789 Controller", 10, 100, COLORS['YELLOW'], 10)
        
        self.lcd.update()
        time.sleep(3)
    
    def demo_colors(self):
        """Демонстрация цветов"""
        print("Демонстрация цветов...")
        
        colors = [
            ('RED', COLORS['RED']),
            ('GREEN', COLORS['GREEN']),
            ('BLUE', COLORS['BLUE']),
            ('YELLOW', COLORS['YELLOW']),
            ('CYAN', COLORS['CYAN']),
            ('MAGENTA', COLORS['MAGENTA'])
        ]
        
        for i, (name, color) in enumerate(colors):
            self.lcd.clear(color)
            self.lcd.draw_text(name, 10, 10, COLORS['WHITE'], 16)
            self.lcd.update()
            time.sleep(1)
    
    def demo_shapes(self):
        """Демонстрация геометрических фигур"""
        print("Демонстрация геометрических фигур...")
        self.lcd.clear()
        
        # Прямоугольники
        self.lcd.draw_rect(10, 10, 50, 30, COLORS['RED'], fill=True)
        self.lcd.draw_rect(70, 10, 50, 30, COLORS['GREEN'], fill=False)
        
        # Круги
        self.lcd.draw_circle(60, 80, 25, COLORS['BLUE'], fill=True)
        self.lcd.draw_circle(150, 80, 25, COLORS['YELLOW'], fill=False)
        
        # Линии
        self.lcd.draw_line(10, 120, 230, 120, COLORS['WHITE'], 3)
        self.lcd.draw_line(10, 130, 230, 150, COLORS['CYAN'], 2)
        
        # Текст
        self.lcd.draw_text("Shapes Demo", 10, 180, COLORS['WHITE'], 14)
        
        self.lcd.update()
        time.sleep(3)
    
    def demo_animation(self):
        """Демонстрация анимации"""
        print("Демонстрация анимации...")
        
        # Анимированный круг
        for i in range(50):
            self.lcd.clear()
            
            # Позиция круга
            x = 120 + int(50 * math.cos(i * 0.2))
            y = 120 + int(30 * math.sin(i * 0.3))
            
            # Рисование круга
            self.lcd.draw_circle(x, y, 20, COLORS['RED'], fill=True)
            
            # След
            for j in range(1, 5):
                trail_x = 120 + int(50 * math.cos((i - j) * 0.2))
                trail_y = 120 + int(30 * math.sin((i - j) * 0.3))
                if 0 <= trail_x < 240 and 0 <= trail_y < 240:
                    self.lcd.draw_circle(trail_x, trail_y, 20 - j * 4, 
                                       COLORS['DARK_GRAY'], fill=True)
            
            self.lcd.update()
            time.sleep(0.05)
    
    def demo_gradient(self):
        """Демонстрация градиента"""
        print("Демонстрация градиента...")
        
        # Создание градиента
        for y in range(240):
            # Градиент от синего к красному
            r = int(255 * y / 240)
            g = 0
            b = int(255 * (240 - y) / 240)
            
            self.lcd.draw_line(0, y, 240, y, (r, g, b), 1)
        
        self.lcd.update()
        time.sleep(2)
    
    def demo_particles(self):
        """Демонстрация частиц"""
        print("Демонстрация частиц...")
        
        import random
        
        # Создание частиц
        particles = []
        for _ in range(20):
            particles.append({
                'x': random.randint(0, 240),
                'y': random.randint(0, 240),
                'vx': random.uniform(-2, 2),
                'vy': random.uniform(-2, 2),
                'life': random.randint(50, 100)
            })
        
        # Анимация частиц
        for frame in range(100):
            self.lcd.clear()
            
            # Обновление частиц
            for particle in particles:
                particle['x'] += particle['vx']
                particle['y'] += particle['vy']
                particle['life'] -= 1
                
                # Отражение от границ
                if particle['x'] <= 0 or particle['x'] >= 240:
                    particle['vx'] *= -1
                if particle['y'] <= 0 or particle['y'] >= 240:
                    particle['vy'] *= -1
                
                # Рисование частицы
                if particle['life'] > 0:
                    size = max(1, particle['life'] // 20)
                    color = (255, 255 - particle['life'] * 2, 0)
                    self.lcd.draw_circle(int(particle['x']), int(particle['y']), 
                                       size, color, fill=True)
            
            # Удаление мертвых частиц и создание новых
            particles = [p for p in particles if p['life'] > 0]
            while len(particles) < 20:
                particles.append({
                    'x': random.randint(0, 240),
                    'y': random.randint(0, 240),
                    'vx': random.uniform(-2, 2),
                    'vy': random.uniform(-2, 2),
                    'life': random.randint(50, 100)
                })
            
            self.lcd.update()
            time.sleep(0.05)
    
    def demo_info(self):
        """Демонстрация информации о системе"""
        print("Демонстрация информации о системе...")
        self.lcd.clear()
        
        # Информация о дисплее
        info_lines = [
            "LCD Game Display",
            "Resolution: 240x240",
            "Controller: ST7789",
            "Interface: SPI",
            "CM4 Compatible",
            "Python Driver"
        ]
        
        y = 20
        for line in info_lines:
            self.lcd.draw_text(line, 10, y, COLORS['WHITE'], 12)
            y += 25
        
        # Статус
        self.lcd.draw_text("Status: OK", 10, 180, COLORS['GREEN'], 14)
        
        self.lcd.update()
        time.sleep(3)
    
    def run_demo(self):
        """Запуск полной демонстрации"""
        print("Запуск демонстрации LCD дисплея...")
        
        try:
            # Последовательность демонстраций
            demos = [
                self.demo_text,
                self.demo_colors,
                self.demo_shapes,
                self.demo_animation,
                self.demo_gradient,
                self.demo_particles,
                self.demo_info
            ]
            
            for demo in demos:
                demo()
                time.sleep(1)
            
            print("Демонстрация завершена!")
            
        except KeyboardInterrupt:
            print("\nДемонстрация прервана пользователем")
        except Exception as e:
            print(f"Ошибка в демонстрации: {e}")
        finally:
            self.lcd.cleanup()


def main():
    """Основная функция"""
    demo = LCDDemo()
    demo.run_demo()


if __name__ == "__main__":
    main()