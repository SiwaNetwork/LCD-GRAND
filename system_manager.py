#!/usr/bin/env python3
"""
Системный менеджер для CM4 LCD Game Driver
Управление поворотом экрана, калибровкой и системной интеграцией
"""

import os
import sys
import subprocess
import shutil
import json
import time
from pathlib import Path
from config import *

class SystemManager:
    """
    Менеджер системной интеграции
    """
    
    def __init__(self):
        """Инициализация системного менеджера"""
        self.config_file = ROTATION_CONFIG['config_file']
        self.calibration_dir = ROTATION_CONFIG['calibration_dir']
        self.current_rotation = ROTATION_CONFIG['current_rotation']
        
    def check_root_permissions(self):
        """Проверка прав администратора"""
        if os.geteuid() != 0:
            print("Ошибка: Требуются права администратора")
            print("Запустите с sudo: sudo python3 system_manager.py")
            return False
        return True
    
    def backup_system_config(self):
        """Резервное копирование системной конфигурации"""
        try:
            backup_dir = SYSTEM_CONFIG['backup_path']
            os.makedirs(backup_dir, exist_ok=True)
            
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            
            # Резервное копирование config.txt
            if os.path.exists(self.config_file):
                backup_file = f"{backup_dir}/config.txt.{timestamp}"
                shutil.copy2(self.config_file, backup_file)
                print(f"✓ Резервная копия config.txt: {backup_file}")
            
            # Резервное копирование калибровки
            calibration_file = f"{self.calibration_dir}/99-calibration.conf"
            if os.path.exists(calibration_file):
                backup_file = f"{backup_dir}/99-calibration.conf.{timestamp}"
                shutil.copy2(calibration_file, backup_file)
                print(f"✓ Резервная копия калибровки: {backup_file}")
            
            return True
            
        except Exception as e:
            print(f"✗ Ошибка резервного копирования: {e}")
            return False
    
    def setup_spi_interface(self):
        """Настройка SPI интерфейса"""
        try:
            # Проверка существующей настройки
            with open(self.config_file, 'r') as f:
                config_content = f.read()
            
            if 'dtparam=spi=on' not in config_content:
                # Добавление настройки SPI
                with open(self.config_file, 'a') as f:
                    f.write('\n# LCD Game Driver SPI Configuration\ndtparam=spi=on\n')
                print("✓ SPI интерфейс включен")
            else:
                print("✓ SPI интерфейс уже настроен")
            
            return True
            
        except Exception as e:
            print(f"✗ Ошибка настройки SPI: {e}")
            return False
    
    def setup_gpio_pullup(self):
        """Настройка подтягивающих резисторов GPIO"""
        try:
            with open(self.config_file, 'r') as f:
                config_content = f.read()
            
            # Добавление подтягивающих резисторов для кнопок
            gpio_pins = ','.join([str(pin) for pin in BUTTON_PINS.values()])
            gpio_config = f"gpio={gpio_pins}=pu"
            
            if gpio_config not in config_content:
                with open(self.config_file, 'a') as f:
                    f.write(f'\n# LCD Game Driver GPIO Configuration\n{gpio_config}\n')
                print("✓ Подтягивающие резисторы GPIO настроены")
            else:
                print("✓ Подтягивающие резисторы GPIO уже настроены")
            
            return True
            
        except Exception as e:
            print(f"✗ Ошибка настройки GPIO: {e}")
            return False
    
    def set_display_rotation(self, angle):
        """
        Установка поворота экрана
        
        Args:
            angle (int): Угол поворота (0, 90, 180, 270)
        """
        if angle not in ROTATION_CONFIG['supported_angles']:
            print(f"✗ Неподдерживаемый угол поворота: {angle}")
            return False
        
        try:
            # Чтение текущей конфигурации
            with open(self.config_file, 'r') as f:
                lines = f.readlines()
            
            # Поиск и замена существующей настройки поворота
            rotation_found = False
            for i, line in enumerate(lines):
                if line.strip().startswith('display_rotate='):
                    lines[i] = f'display_rotate={angle}\n'
                    rotation_found = True
                    break
            
            # Добавление новой настройки, если не найдена
            if not rotation_found:
                lines.append(f'display_rotate={angle}\n')
            
            # Запись обновленной конфигурации
            with open(self.config_file, 'w') as f:
                f.writelines(lines)
            
            # Обновление калибровки сенсора
            self.update_touch_calibration(angle)
            
            self.current_rotation = angle
            print(f"✓ Поворот экрана установлен на {angle}°")
            return True
            
        except Exception as e:
            print(f"✗ Ошибка установки поворота: {e}")
            return False
    
    def update_touch_calibration(self, angle):
        """
        Обновление калибровки сенсора
        
        Args:
            angle (int): Угол поворота
        """
        try:
            # Создание директории, если не существует
            os.makedirs(self.calibration_dir, exist_ok=True)
            
            # Получение матрицы калибровки
            calibration_matrix = CALIBRATION_CONFIG['calibration_matrix'].get(angle, '268 3880 227 3936')
            
            # Создание конфигурационного файла калибровки
            calibration_content = f"""Section "InputClass"
        Identifier      "calibration"
        MatchProduct    "{CALIBRATION_CONFIG['touch_device']}"
        Option  "Calibration"   "{calibration_matrix}"
        Option  "SwapAxes"      "{'1' if CALIBRATION_CONFIG['swap_axes'] else '0'}"
        Option "EmulateThirdButton" "{'1' if CALIBRATION_CONFIG['emulate_third_button'] else '0'}"
        Option "EmulateThirdButtonTimeout" "{CALIBRATION_CONFIG['third_button_timeout']}"
        Option "EmulateThirdButtonMoveThreshold" "{CALIBRATION_CONFIG['third_button_threshold']}"
EndSection
"""
            
            # Запись файла калибровки
            calibration_file = f"{self.calibration_dir}/99-calibration.conf"
            with open(calibration_file, 'w') as f:
                f.write(calibration_content)
            
            print(f"✓ Калибровка сенсора обновлена для поворота {angle}°")
            return True
            
        except Exception as e:
            print(f"✗ Ошибка обновления калибровки: {e}")
            return False
    
    def get_current_rotation(self):
        """Получение текущего поворота экрана"""
        try:
            with open(self.config_file, 'r') as f:
                config_content = f.read()
            
            for line in config_content.split('\n'):
                if line.strip().startswith('display_rotate='):
                    angle = int(line.split('=')[1].strip())
                    self.current_rotation = angle
                    return angle
            
            return 0
            
        except Exception as e:
            print(f"✗ Ошибка получения поворота: {e}")
            return 0
    
    def install_systemd_service(self):
        """Установка systemd сервиса"""
        try:
            service_content = f"""[Unit]
Description=LCD Game Driver Service
After=network.target

[Service]
Type=simple
User={SYSTEM_CONFIG['service_user']}
Group={SYSTEM_CONFIG['service_group']}
WorkingDirectory={SYSTEM_CONFIG['install_path']}
Environment=PATH={SYSTEM_CONFIG['install_path']}/venv/bin
ExecStart={SYSTEM_CONFIG['install_path']}/venv/bin/python3 {SYSTEM_CONFIG['install_path']}/main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
"""
            
            service_file = f"/etc/systemd/system/{SYSTEM_CONFIG['service_name']}.service"
            with open(service_file, 'w') as f:
                f.write(service_content)
            
            # Перезагрузка systemd
            subprocess.run(['systemctl', 'daemon-reload'], check=True)
            
            # Включение автозапуска
            subprocess.run(['systemctl', 'enable', f'{SYSTEM_CONFIG["service_name"]}.service'], check=True)
            
            print("✓ Systemd сервис установлен и включен")
            return True
            
        except Exception as e:
            print(f"✗ Ошибка установки systemd сервиса: {e}")
            return False
    
    def install_autostart(self):
        """Установка автозапуска"""
        try:
            autostart_dir = os.path.expanduser(SYSTEM_CONFIG['autostart_path'])
            os.makedirs(autostart_dir, exist_ok=True)
            
            desktop_content = f"""[Desktop Entry]
Type=Application
Name=LCD Game Driver
Comment=LCD Game Driver for CM4
Exec={SYSTEM_CONFIG['install_path']}/venv/bin/python3 {SYSTEM_CONFIG['install_path']}/main.py
Terminal=false
X-GNOME-Autostart-enabled=true
"""
            
            desktop_file = f"{autostart_dir}/lcd-game.desktop"
            with open(desktop_file, 'w') as f:
                f.write(desktop_content)
            
            print("✓ Автозапуск настроен")
            return True
            
        except Exception as e:
            print(f"✗ Ошибка настройки автозапуска: {e}")
            return False
    
    def install_pymouse(self):
        """Установка PyMouse для эмуляции мыши"""
        try:
            # Проверка установки PyMouse
            try:
                import pymouse
                print("✓ PyMouse уже установлен")
                return True
            except ImportError:
                pass
            
            # Установка PyMouse
            subprocess.run([sys.executable, '-m', 'pip', 'install', 'PyMouse'], check=True)
            print("✓ PyMouse установлен")
            return True
            
        except Exception as e:
            print(f"✗ Ошибка установки PyMouse: {e}")
            return False
    
    def create_mouse_emulator(self):
        """Создание эмулятора мыши"""
        try:
            mouse_script = f"""#!/usr/bin/env python3
\"\"\"
Эмулятор мыши для LCD Game Driver
\"\"\"

from pymouse import PyMouse
import time
import RPi.GPIO as GPIO
from config import *

GPIO.setmode(GPIO.BCM)

# Настройка кнопок
for button_name, pin in BUTTON_PINS.items():
    GPIO.setup(pin, GPIO.IN, GPIO.PUD_UP)

def main():
    m = PyMouse()
    button_flags = {{}}
    
    for button_name in BUTTON_PINS.keys():
        button_flags[button_name] = False
    
    print("Эмулятор мыши запущен...")
    
    while True:
        current_pos = m.position()
        
        # Обработка кнопок
        for button_name, pin in BUTTON_PINS.items():
            if not GPIO.input(pin):  # Кнопка нажата
                if not button_flags[button_name]:
                    button_flags[button_name] = True
                    
                    if button_name in ['A', 'B']:
                        # Эмуляция клика
                        click_type = 1 if button_name == 'A' else 2
                        m.click(current_pos[0], current_pos[1], click_type)
                        print(f"Клик: {{button_name}}")
                    else:
                        # Эмуляция движения мыши
                        move_speed = MOUSE_CONFIG['move_speed']
                        if button_name == 'UP':
                            m.move(current_pos[0], current_pos[1] - move_speed)
                        elif button_name == 'DOWN':
                            m.move(current_pos[0], current_pos[1] + move_speed)
                        elif button_name == 'LEFT':
                            m.move(current_pos[0] - move_speed, current_pos[1])
                        elif button_name == 'RIGHT':
                            m.move(current_pos[0] + move_speed, current_pos[1])
                        
                        print(f"Движение: {{button_name}}")
            
            elif button_flags[button_name]:  # Кнопка отпущена
                button_flags[button_name] = False
        
        time.sleep(MOUSE_CONFIG['poll_interval'])

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\\nЭмулятор мыши остановлен")
        GPIO.cleanup()
"""
            
            mouse_file = f"{SYSTEM_CONFIG['install_path']}/mouse_emulator.py"
            with open(mouse_file, 'w') as f:
                f.write(mouse_script)
            
            # Установка прав на выполнение
            os.chmod(mouse_file, 0o755)
            
            print("✓ Эмулятор мыши создан")
            return True
            
        except Exception as e:
            print(f"✗ Ошибка создания эмулятора мыши: {e}")
            return False
    
    def test_system_integration(self):
        """Тестирование системной интеграции"""
        try:
            print("Тестирование системной интеграции...")
            
            # Проверка SPI
            if not os.path.exists('/dev/spidev0.0'):
                print("✗ SPI устройство не найдено")
                return False
            
            # Проверка GPIO
            try:
                import RPi.GPIO as GPIO
                GPIO.setmode(GPIO.BCM)
                GPIO.cleanup()
                print("✓ GPIO доступен")
            except Exception as e:
                print(f"✗ Ошибка GPIO: {e}")
                return False
            
            # Проверка поворота
            current_rotation = self.get_current_rotation()
            print(f"✓ Текущий поворот: {current_rotation}°")
            
            # Проверка калибровки
            calibration_file = f"{self.calibration_dir}/99-calibration.conf"
            if os.path.exists(calibration_file):
                print("✓ Файл калибровки найден")
            else:
                print("⚠ Файл калибровки не найден")
            
            print("✓ Системная интеграция работает")
            return True
            
        except Exception as e:
            print(f"✗ Ошибка тестирования: {e}")
            return False

def main():
    """Главная функция"""
    if not os.geteuid() == 0:
        print("Ошибка: Требуются права администратора")
        print("Запустите: sudo python3 system_manager.py")
        sys.exit(1)
    
    manager = SystemManager()
    
    print("=" * 50)
    print("Системный менеджер LCD Game Driver")
    print("=" * 50)
    
    # Резервное копирование
    manager.backup_system_config()
    
    # Настройка системы
    manager.setup_spi_interface()
    manager.setup_gpio_pullup()
    
    # Установка сервисов
    manager.install_systemd_service()
    manager.install_autostart()
    manager.install_pymouse()
    manager.create_mouse_emulator()
    
    # Тестирование
    manager.test_system_integration()
    
    print("\n" + "=" * 50)
    print("Установка завершена!")
    print("Перезагрузите систему: sudo reboot")
    print("=" * 50)

if __name__ == "__main__":
    main()