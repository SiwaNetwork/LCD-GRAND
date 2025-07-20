#!/usr/bin/env python3
"""
1.54 inch LCD GAME Driver for CM4
Поддержка ST7789 контроллера через SPI интерфейс
"""

import time
import spidev
import RPi.GPIO as GPIO
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from config import *

class LCDGame:
    """
    Драйвер для 1.54 inch LCD GAME дисплея на CM4
    """
    
    def __init__(self, rotation=0, spi_bus=SPI_BUS, spi_device=SPI_DEVICE):
        """
        Инициализация драйвера LCD дисплея
        
        Args:
            rotation (int): Поворот дисплея (0, 90, 180, 270)
            spi_bus (int): Номер SPI шины
            spi_device (int): Номер SPI устройства
        """
        self.width = DISPLAY_WIDTH
        self.height = DISPLAY_HEIGHT
        self.rotation = rotation
        
        # Настройка GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PIN_RESET, GPIO.OUT)
        GPIO.setup(PIN_DC, GPIO.OUT)
        GPIO.setup(PIN_CS, GPIO.OUT)
        GPIO.setup(PIN_BACKLIGHT, GPIO.OUT)
        
        # Настройка SPI
        self.spi = spidev.SpiDev()
        self.spi.open(spi_bus, spi_device)
        self.spi.max_speed_hz = SPI_SPEED
        self.spi.mode = 0
        
        # Инициализация дисплея
        self._init_display()
        
        # Создание буфера изображения
        self.buffer = Image.new('RGB', (self.width, self.height), color=(0, 0, 0))
        self.draw = ImageDraw.Draw(self.buffer)
        
        # Включение подсветки
        GPIO.output(PIN_BACKLIGHT, GPIO.HIGH)
        
    def _init_display(self):
        """Инициализация дисплея ST7789"""
        # Сброс дисплея
        GPIO.output(PIN_RESET, GPIO.HIGH)
        time.sleep(0.01)
        GPIO.output(PIN_RESET, GPIO.LOW)
        time.sleep(0.01)
        GPIO.output(PIN_RESET, GPIO.HIGH)
        time.sleep(0.01)
        
        # Команды инициализации ST7789
        init_commands = [
            (0x11, None),  # Sleep out
            (0x36, [0x00]),  # Memory Access Control
            (0x3A, [0x05]),  # Interface Pixel Format
            (0x2A, [0x00, 0x00, 0x00, 0xEF]),  # Column Address Set
            (0x2B, [0x00, 0x00, 0x00, 0xEF]),  # Row Address Set
            (0x2C, None),  # Memory Write
            (0xB2, [0x0C, 0x0C, 0x00, 0x33, 0x33]),  # Porch Setting
            (0xB7, [0x35]),  # Gate Control
            (0xBB, [0x19]),  # VCOM Setting
            (0xC0, [0x2C]),  # LCM Control
            (0xC2, [0x01]),  # VDV and VRH Command Enable
            (0xC3, [0x12]),  # VRH Set
            (0xC4, [0x20]),  # VDV Set
            (0xC6, [0x0F]),  # Frame Rate Control in Normal Mode
            (0xD0, [0xA4, 0xA1]),  # Power Control 1
            (0xE0, [0xD0, 0x04, 0x0D, 0x11, 0x13, 0x2B, 0x3F, 0x54, 0x4C, 0x18, 0x0D, 0x0B, 0x1F, 0x23]),  # Positive Voltage Gamma Control
            (0xE1, [0xD0, 0x04, 0x0C, 0x11, 0x13, 0x2C, 0x3F, 0x44, 0x51, 0x2F, 0x1F, 0x1F, 0x20, 0x23]),  # Negative Voltage Gamma Control
            (0x21, None),  # Display Inversion On
            (0x29, None),  # Display On
        ]
        
        for cmd, data in init_commands:
            self._write_command(cmd)
            if data:
                self._write_data(data)
            time.sleep(0.01)
    
    def _write_command(self, cmd):
        """Отправка команды на дисплей"""
        GPIO.output(PIN_DC, GPIO.LOW)
        GPIO.output(PIN_CS, GPIO.LOW)
        self.spi.writebytes([cmd])
        GPIO.output(PIN_CS, GPIO.HIGH)
    
    def _write_data(self, data):
        """Отправка данных на дисплей"""
        GPIO.output(PIN_DC, GPIO.HIGH)
        GPIO.output(PIN_CS, GPIO.LOW)
        if isinstance(data, list):
            self.spi.writebytes(data)
        else:
            self.spi.writebytes([data])
        GPIO.output(PIN_CS, GPIO.HIGH)
    
    def _set_window(self, x_start, y_start, x_end, y_end):
        """Установка области отображения"""
        # Column Address Set
        self._write_command(0x2A)
        self._write_data([x_start >> 8, x_start & 0xFF, x_end >> 8, x_end & 0xFF])
        
        # Row Address Set
        self._write_command(0x2B)
        self._write_data([y_start >> 8, y_start & 0xFF, y_end >> 8, y_end & 0xFF])
        
        # Memory Write
        self._write_command(0x2C)
    
    def clear(self, color=(0, 0, 0)):
        """Очистка экрана"""
        self.buffer = Image.new('RGB', (self.width, self.height), color=color)
        self.draw = ImageDraw.Draw(self.buffer)
        self.update()
    
    def update(self):
        """Обновление дисплея"""
        # Конвертация RGB в RGB565
        img_data = self.buffer.convert('RGB')
        pixels = list(img_data.getdata())
        
        # Установка области отображения
        self._set_window(0, 0, self.width - 1, self.height - 1)
        
        # Подготовка данных для отправки
        data = []
        for pixel in pixels:
            r, g, b = pixel
            # Конвертация в RGB565
            rgb565 = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
            data.extend([rgb565 >> 8, rgb565 & 0xFF])
        
        # Отправка данных
        GPIO.output(PIN_DC, GPIO.HIGH)
        GPIO.output(PIN_CS, GPIO.LOW)
        self.spi.writebytes(data)
        GPIO.output(PIN_CS, GPIO.HIGH)
    
    def draw_pixel(self, x, y, color=(255, 255, 255)):
        """Рисование пикселя"""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.buffer.putpixel((x, y), color)
    
    def draw_line(self, x1, y1, x2, y2, color=(255, 255, 255), width=1):
        """Рисование линии"""
        self.draw.line([(x1, y1), (x2, y2)], fill=color, width=width)
    
    def draw_rect(self, x, y, width, height, color=(255, 255, 255), fill=None):
        """Рисование прямоугольника"""
        if fill:
            self.draw.rectangle([x, y, x + width - 1, y + height - 1], fill=color, outline=color)
        else:
            self.draw.rectangle([x, y, x + width - 1, y + height - 1], outline=color)
    
    def draw_circle(self, x, y, radius, color=(255, 255, 255), fill=None):
        """Рисование окружности"""
        bbox = [x - radius, y - radius, x + radius, y + radius]
        if fill:
            self.draw.ellipse(bbox, fill=color, outline=color)
        else:
            self.draw.ellipse(bbox, outline=color)
    
    def draw_text(self, text, x, y, color=(255, 255, 255), font_size=12):
        """Рисование текста"""
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        self.draw.text((x, y), text, fill=color, font=font)
    
    def draw_image(self, image_path, x, y):
        """Отображение изображения"""
        try:
            img = Image.open(image_path)
            self.buffer.paste(img, (x, y))
        except Exception as e:
            print(f"Ошибка загрузки изображения: {e}")
    
    def set_backlight(self, state):
        """Управление подсветкой"""
        GPIO.output(PIN_BACKLIGHT, GPIO.HIGH if state else GPIO.LOW)
    
    def get_buffer(self):
        """Получение текущего буфера изображения"""
        return self.buffer
    
    def set_buffer(self, image):
        """Установка буфера изображения"""
        if image.size == (self.width, self.height):
            self.buffer = image
            self.draw = ImageDraw.Draw(self.buffer)
    
    def cleanup(self):
        """Очистка ресурсов"""
        GPIO.cleanup()
        self.spi.close()


class GameEngine:
    """
    Игровой движок для создания игр на LCD дисплее
    """
    
    def __init__(self, lcd):
        """
        Инициализация игрового движка
        
        Args:
            lcd: Экземпляр LCDGame
        """
        self.lcd = lcd
        self.running = False
        self.fps = 30
        self.last_frame_time = time.time()
    
    def start(self):
        """Запуск игрового цикла"""
        self.running = True
        self.game_loop()
    
    def stop(self):
        """Остановка игрового цикла"""
        self.running = False
    
    def game_loop(self):
        """Основной игровой цикл"""
        while self.running:
            current_time = time.time()
            delta_time = current_time - self.last_frame_time
            
            if delta_time >= 1.0 / self.fps:
                self.update(delta_time)
                self.render()
                self.last_frame_time = current_time
            
            time.sleep(0.001)  # Небольшая задержка для снижения нагрузки на CPU
    
    def update(self, delta_time):
        """Обновление игровой логики (переопределить в наследниках)"""
        pass
    
    def render(self):
        """Отрисовка (переопределить в наследниках)"""
        pass


# Примеры использования
if __name__ == "__main__":
    try:
        # Создание экземпляра дисплея
        lcd = LCDGame()
        
        # Очистка экрана
        lcd.clear()
        
        # Рисование тестового изображения
        lcd.draw_text("Hello CM4!", 10, 10, color=(255, 255, 255))
        lcd.draw_rect(50, 50, 100, 50, color=(255, 0, 0), fill=True)
        lcd.draw_circle(150, 150, 30, color=(0, 255, 0), fill=True)
        lcd.draw_line(0, 0, 240, 240, color=(0, 0, 255), width=3)
        
        # Обновление дисплея
        lcd.update()
        
        print("Тест дисплея завершен. Нажмите Ctrl+C для выхода.")
        
        # Ожидание
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nЗавершение работы...")
        lcd.cleanup()
    except Exception as e:
        print(f"Ошибка: {e}")
        lcd.cleanup()