#!/usr/bin/env python3
"""
Главный файл системы CM4 с LCD дисплеем
Объединяет заставку включения и рабочий стол
"""

import sys
import time
import signal
import os
from lcd_game import LCDGame
from boot_splash import BootSplash
from desktop import Desktop

class CM4System:
    """
    Главный класс системы CM4
    """
    
    def __init__(self):
        """Инициализация системы"""
        self.lcd = None
        self.splash = None
        self.desktop = None
        self.running = True
        
        # Обработка сигналов для корректного завершения
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def signal_handler(self, signum, frame):
        """Обработчик сигналов для корректного завершения"""
        print(f"\nПолучен сигнал {signum}, завершение работы...")
        self.running = False
        self.cleanup()
        sys.exit(0)
    
    def initialize_system(self):
        """Инициализация системы"""
        try:
            print("Инициализация системы CM4...")
            
            # Инициализация LCD дисплея
            self.lcd = LCDGame()
            print("LCD дисплей инициализирован")
            
            # Инициализация заставки
            self.splash = BootSplash(self.lcd)
            print("Заставка инициализирована")
            
            # Инициализация рабочего стола
            self.desktop = Desktop(self.lcd)
            print("Рабочий стол инициализирован")
            
            return True
            
        except Exception as e:
            print(f"Ошибка инициализации системы: {e}")
            return False
    
    def show_boot_splash(self):
        """Показ заставки включения"""
        try:
            print("Запуск заставки включения...")
            self.splash.run()
            print("Заставка завершена")
            return True
        except Exception as e:
            print(f"Ошибка заставки: {e}")
            return False
    
    def start_desktop(self):
        """Запуск рабочего стола"""
        try:
            print("Запуск рабочего стола...")
            self.desktop.run()
        except Exception as e:
            print(f"Ошибка рабочего стола: {e}")
    
    def run(self):
        """Основной цикл работы системы"""
        try:
            # Инициализация
            if not self.initialize_system():
                print("Ошибка инициализации системы")
                return
            
            # Показ заставки
            if not self.show_boot_splash():
                print("Ошибка заставки")
                return
            
            # Запуск рабочего стола
            self.start_desktop()
            
        except KeyboardInterrupt:
            print("Система остановлена пользователем")
        except Exception as e:
            print(f"Критическая ошибка системы: {e}")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Очистка ресурсов"""
        try:
            if self.lcd:
                print("Очистка LCD дисплея...")
                self.lcd.cleanup()
                print("LCD дисплей очищен")
        except Exception as e:
            print(f"Ошибка очистки: {e}")

def check_dependencies():
    """Проверка зависимостей"""
    try:
        import psutil
        import RPi.GPIO as GPIO
        import spidev
        from PIL import Image, ImageDraw, ImageFont
        print("Все зависимости доступны")
        return True
    except ImportError as e:
        print(f"Отсутствует зависимость: {e}")
        print("Установите зависимости: pip3 install -r requirements.txt")
        return False

def check_permissions():
    """Проверка прав доступа"""
    try:
        # Проверка доступа к GPIO
        import RPi.GPIO as GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.cleanup()
        print("Права доступа к GPIO в порядке")
        return True
    except Exception as e:
        print(f"Ошибка прав доступа: {e}")
        print("Запустите с правами sudo: sudo python3 main.py")
        return False

def main():
    """Главная функция"""
    print("=" * 50)
    print("SHIWA NETWORK Grand Mini - CM4 System")
    print("=" * 50)
    
    # Проверка зависимостей
    if not check_dependencies():
        sys.exit(1)
    
    # Проверка прав доступа
    if not check_permissions():
        sys.exit(1)
    
    # Создание и запуск системы
    system = CM4System()
    system.run()

if __name__ == "__main__":
    main()