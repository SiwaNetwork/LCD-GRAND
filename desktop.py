#!/usr/bin/env python3
"""
Рабочий стол для CM4 с LCD дисплеем
Основной интерфейс системы
"""

import time
import datetime
import psutil
import os
from lcd_game import LCDGame
from config import *

class Desktop:
    """
    Класс рабочего стола
    """
    
    def __init__(self, lcd):
        """
        Инициализация рабочего стола
        
        Args:
            lcd: Экземпляр LCDGame
        """
        self.lcd = lcd
        self.width = DISPLAY_WIDTH
        self.height = DISPLAY_HEIGHT
        self.current_screen = "main"
        self.selected_item = 0
        self.menu_items = [
            {"name": "System Info", "icon": "📊"},
            {"name": "Games", "icon": "🎮"},
            {"name": "Settings", "icon": "⚙️"},
            {"name": "Network", "icon": "🌐"},
            {"name": "Shutdown", "icon": "⏻"}
        ]
        self.last_update = 0
        self.update_interval = 1.0  # Обновление каждую секунду
    
    def draw_status_bar(self):
        """Отрисовка верхней панели статуса"""
        # Фон панели
        self.lcd.draw_rect(0, 0, self.width, 25, color=(40, 40, 40), fill=True)
        
        # Время
        current_time = datetime.datetime.now().strftime("%H:%M")
        self.lcd.draw_text(current_time, 10, 5, color=(255, 255, 255), font_size=12)
        
        # Индикатор сети
        self.lcd.draw_text("📶", self.width - 30, 5, color=(0, 255, 0), font_size=12)
        
        # Индикатор батареи (симуляция)
        battery_level = 85  # В реальной системе получать из системы
        battery_color = (0, 255, 0) if battery_level > 50 else (255, 255, 0) if battery_level > 20 else (255, 0, 0)
        self.lcd.draw_text(f"🔋{battery_level}%", self.width - 80, 5, color=battery_color, font_size=10)
    
    def draw_main_screen(self):
        """Отрисовка главного экрана"""
        # Очистка экрана
        self.lcd.clear()
        
        # Статус бар
        self.draw_status_bar()
        
        # Заголовок
        self.lcd.draw_text("SHIWA NETWORK", 10, 35, color=(0, 150, 255), font_size=14)
        self.lcd.draw_text("Grand Mini", 10, 50, color=(100, 100, 100), font_size=12)
        
        # Основная информация
        self.draw_system_info()
        
        # Меню
        self.draw_menu()
    
    def draw_system_info(self):
        """Отрисовка системной информации"""
        try:
            # CPU
            cpu_percent = psutil.cpu_percent(interval=0.1)
            self.lcd.draw_text(f"CPU: {cpu_percent}%", 10, 80, color=(255, 255, 255), font_size=10)
            
            # Память
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            self.lcd.draw_text(f"RAM: {memory_percent}%", 10, 95, color=(255, 255, 255), font_size=10)
            
            # Температура (симуляция)
            temp = 45  # В реальной системе получать из /sys/class/thermal/
            self.lcd.draw_text(f"TEMP: {temp}°C", 10, 110, color=(255, 255, 255), font_size=10)
            
            # Uptime
            uptime = datetime.datetime.now() - datetime.datetime.fromtimestamp(psutil.boot_time())
            uptime_str = str(uptime).split('.')[0]  # Убираем микросекунды
            self.lcd.draw_text(f"UP: {uptime_str}", 10, 125, color=(255, 255, 255), font_size=10)
            
        except Exception as e:
            self.lcd.draw_text("System info error", 10, 80, color=(255, 0, 0), font_size=10)
    
    def draw_menu(self):
        """Отрисовка меню"""
        menu_y = 150
        item_height = 20
        
        for i, item in enumerate(self.menu_items):
            y_pos = menu_y + i * item_height
            
            # Выделение выбранного элемента
            if i == self.selected_item:
                self.lcd.draw_rect(5, y_pos - 2, self.width - 10, item_height, color=(0, 150, 255), fill=True)
                text_color = (255, 255, 255)
            else:
                text_color = (200, 200, 200)
            
            # Иконка и текст
            self.lcd.draw_text(item["icon"], 10, y_pos, color=text_color, font_size=12)
            self.lcd.draw_text(item["name"], 35, y_pos, color=text_color, font_size=12)
    
    def draw_system_info_screen(self):
        """Экран системной информации"""
        self.lcd.clear()
        self.draw_status_bar()
        
        self.lcd.draw_text("System Information", 10, 35, color=(0, 150, 255), font_size=14)
        
        try:
            # Подробная информация о системе
            info_items = [
                f"CPU: {psutil.cpu_percent()}%",
                f"RAM: {psutil.virtual_memory().percent}%",
                f"Disk: {psutil.disk_usage('/').percent}%",
                f"Load: {os.getloadavg()[0]:.2f}",
                f"Processes: {len(psutil.pids())}",
                f"Network: Active"
            ]
            
            for i, item in enumerate(info_items):
                y_pos = 60 + i * 20
                self.lcd.draw_text(item, 10, y_pos, color=(255, 255, 255), font_size=10)
        
        except Exception as e:
            self.lcd.draw_text("Error loading system info", 10, 60, color=(255, 0, 0), font_size=10)
    
    def draw_games_screen(self):
        """Экран игр"""
        self.lcd.clear()
        self.draw_status_bar()
        
        self.lcd.draw_text("Games", 10, 35, color=(0, 150, 255), font_size=14)
        
        games = [
            {"name": "Snake Game", "icon": "🐍"},
            {"name": "Pong", "icon": "🏓"},
            {"name": "Tetris", "icon": "🧩"},
            {"name": "Breakout", "icon": "🏀"}
        ]
        
        for i, game in enumerate(games):
            y_pos = 60 + i * 30
            self.lcd.draw_text(game["icon"], 10, y_pos, color=(255, 255, 255), font_size=12)
            self.lcd.draw_text(game["name"], 35, y_pos, color=(255, 255, 255), font_size=12)
    
    def draw_settings_screen(self):
        """Экран настроек"""
        self.lcd.clear()
        self.draw_status_bar()
        
        self.lcd.draw_text("Settings", 10, 35, color=(0, 150, 255), font_size=14)
        
        settings = [
            {"name": "Display Brightness", "value": "80%"},
            {"name": "Sound Volume", "value": "70%"},
            {"name": "Auto Sleep", "value": "5min"},
            {"name": "Network Config", "value": "WiFi"},
            {"name": "System Update", "value": "Available"}
        ]
        
        for i, setting in enumerate(settings):
            y_pos = 60 + i * 25
            self.lcd.draw_text(setting["name"], 10, y_pos, color=(255, 255, 255), font_size=10)
            self.lcd.draw_text(setting["value"], self.width - 60, y_pos, color=(100, 100, 100), font_size=10)
    
    def draw_network_screen(self):
        """Экран сетевых настроек"""
        self.lcd.clear()
        self.draw_status_bar()
        
        self.lcd.draw_text("Network Status", 10, 35, color=(0, 150, 255), font_size=14)
        
        # Сетевая информация
        network_info = [
            "WiFi: Connected",
            "SSID: SHIWA_Network",
            "IP: 192.168.1.100",
            "Signal: -45 dBm",
            "Speed: 54 Mbps",
            "Uptime: 2h 15m"
        ]
        
        for i, info in enumerate(network_info):
            y_pos = 60 + i * 20
            self.lcd.draw_text(info, 10, y_pos, color=(255, 255, 255), font_size=10)
    
    def draw_shutdown_screen(self):
        """Экран выключения"""
        self.lcd.clear()
        
        # Центрированный текст
        self.lcd.draw_text("Shutdown System?", self.width // 2 - 70, self.height // 2 - 30, color=(255, 255, 255), font_size=14)
        self.lcd.draw_text("Press A to confirm", self.width // 2 - 60, self.height // 2, color=(200, 200, 200), font_size=12)
        self.lcd.draw_text("Press B to cancel", self.width // 2 - 60, self.height // 2 + 20, color=(200, 200, 200), font_size=12)
    
    def handle_input(self):
        """Обработка ввода пользователя"""
        # Навигация по меню
        if self.lcd.buttons.is_pressed('UP'):
            if self.current_screen == "main":
                self.selected_item = max(0, self.selected_item - 1)
            return True
        
        if self.lcd.buttons.is_pressed('DOWN'):
            if self.current_screen == "main":
                self.selected_item = min(len(self.menu_items) - 1, self.selected_item + 1)
            return True
        
        if self.lcd.buttons.is_pressed('A'):
            if self.current_screen == "main":
                # Выбор пункта меню
                selected_menu = self.menu_items[self.selected_item]["name"]
                if selected_menu == "System Info":
                    self.current_screen = "system_info"
                elif selected_menu == "Games":
                    self.current_screen = "games"
                elif selected_menu == "Settings":
                    self.current_screen = "settings"
                elif selected_menu == "Network":
                    self.current_screen = "network"
                elif selected_menu == "Shutdown":
                    self.current_screen = "shutdown"
            elif self.current_screen == "shutdown":
                # Подтверждение выключения
                os.system("sudo shutdown -h now")
            return True
        
        if self.lcd.buttons.is_pressed('B'):
            if self.current_screen != "main":
                self.current_screen = "main"
                self.selected_item = 0
            return True
        
        return False
    
    def update(self):
        """Обновление экрана"""
        current_time = time.time()
        
        # Обновление каждую секунду
        if current_time - self.last_update >= self.update_interval:
            self.last_update = current_time
            
            # Отрисовка соответствующего экрана
            if self.current_screen == "main":
                self.draw_main_screen()
            elif self.current_screen == "system_info":
                self.draw_system_info_screen()
            elif self.current_screen == "games":
                self.draw_games_screen()
            elif self.current_screen == "settings":
                self.draw_settings_screen()
            elif self.current_screen == "network":
                self.draw_network_screen()
            elif self.current_screen == "shutdown":
                self.draw_shutdown_screen()
            
            self.lcd.update()
    
    def run(self):
        """Запуск рабочего стола"""
        try:
            print("Запуск рабочего стола...")
            
            while True:
                # Обработка ввода
                if self.handle_input():
                    # Принудительное обновление при изменении
                    self.last_update = 0
                
                # Обновление экрана
                self.update()
                
                # Небольшая задержка
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            print("Рабочий стол остановлен")
        except Exception as e:
            print(f"Ошибка в рабочем столе: {e}")

if __name__ == "__main__":
    # Тест рабочего стола
    lcd = LCDGame()
    desktop = Desktop(lcd)
    desktop.run()
    lcd.cleanup()