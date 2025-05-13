import sys
import json
from PyQt5.QtWidgets import QApplication
from gui import MainWindow
from modbus_handler import ModbusHandler
from mqtt_handler import MQTTHandler

def load_config():
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading config: {str(e)}")
        return None

def main():
    app = QApplication(sys.argv)
    
    # Load configuration
    config = load_config()
    
    # Initialize handlers with config
    modbus_handler = ModbusHandler(
        com=config['modbus']['com'],
        baudrate=config['modbus']['baudrate'],
        timeout=config['modbus']['timeout']
    ) if config else ModbusHandler()
    
    mqtt_handler = MQTTHandler(
        broker=config['mqtt']['broker'],
        port=config['mqtt']['port'],
        username=config['mqtt']['username'],
        password=config['mqtt']['password']
    ) if config else MQTTHandler()
    
    # Create and show the main window
    window = MainWindow(modbus_handler, mqtt_handler)
    window.show()
    
    return app.exec_()

if __name__ == '__main__':
    sys.exit(main())