from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                           QPushButton, QLineEdit, QLabel, QTextEdit, QGridLayout,
                           QCheckBox, QMessageBox)
from PyQt5.QtCore import QTimer
from datetime import datetime

class MainWindow(QMainWindow):
    def __init__(self, modbus_handler, mqtt_handler):
        super().__init__()
        self.modbus_handler = modbus_handler
        self.mqtt_handler = mqtt_handler
        self.show_mqtt_timestamp = False
        self.show_modbus_timestamp = False
        self.initUI()  # Changed from init_ui to initUI
        # Set initial values from mqtt_handler
        self.mqtt_broker.setText(self.mqtt_handler.broker)
        self.mqtt_port.setText(str(self.mqtt_handler.port))
        # Set initial values from modbus_handler
        self.modbus_host.setText(self.modbus_handler.com)
        self.modbus_port.setText(str(self.modbus_handler.baudrate))
        
        # Apply styles to buttons
        self.apply_styles()

    def initUI(self):  # Changed from init_ui to initUI
        self.setWindowTitle('Modbus and MQTT GUI')
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)

        self.modbus_layout = QGridLayout()
        self.main_layout.addLayout(self.modbus_layout)

        self.modbus_host_label = QLabel('Modbus Host:')
        self.modbus_layout.addWidget(self.modbus_host_label, 0, 0)

        self.modbus_host = QLineEdit()
        self.modbus_layout.addWidget(self.modbus_host, 0, 1)

        self.modbus_port_label = QLabel('Modbus Port:')
        self.modbus_layout.addWidget(self.modbus_port_label, 0, 2)

        self.modbus_port = QLineEdit()
        self.modbus_layout.addWidget(self.modbus_port, 0, 3)

        self.modbus_read_button = QPushButton('Read Modbus')    
        self.modbus_read_button.clicked.connect(self.read_modbus)
        self.modbus_layout.addWidget(self.modbus_read_button, 0, 4)

        # Add Modbus data input section
        self.modbus_input_layout = QHBoxLayout()
        self.modbus_layout.addLayout(self.modbus_input_layout, 1, 0, 1, 5)

        self.modbus_address_label = QLabel('Register Address:')
        self.modbus_input_layout.addWidget(self.modbus_address_label)

        self.modbus_address = QLineEdit()
        self.modbus_address.setPlaceholderText('e.g. 4096 (0x1000)')
        self.modbus_input_layout.addWidget(self.modbus_address)

        self.modbus_value_label = QLabel('Value:')
        self.modbus_input_layout.addWidget(self.modbus_value_label)

        self.modbus_value = QLineEdit()
        self.modbus_value.setPlaceholderText('Enter value to write')
        self.modbus_input_layout.addWidget(self.modbus_value)

        self.modbus_write_button = QPushButton('Write Modbus')
        self.modbus_write_button.clicked.connect(self.write_modbus)
        self.modbus_input_layout.addWidget(self.modbus_write_button)

        self.modbus_data_label = QLabel('Modbus Data:')
        self.modbus_layout.addWidget(self.modbus_data_label, 2, 0, 1, 5)

        self.modbus_data = QTextEdit()
        self.modbus_layout.addWidget(self.modbus_data, 3, 0, 1, 5)

        self.mqtt_layout = QGridLayout()
        self.main_layout.addLayout(self.mqtt_layout)

        # MQTT Connection Section
        self.mqtt_broker_label = QLabel('MQTT Broker:')
        self.mqtt_layout.addWidget(self.mqtt_broker_label, 0, 0)            
        self.mqtt_broker = QLineEdit()
        self.mqtt_layout.addWidget(self.mqtt_broker, 0, 1)

        self.mqtt_port_label = QLabel('MQTT Port:')
        self.mqtt_layout.addWidget(self.mqtt_port_label, 0, 2)
        self.mqtt_port = QLineEdit()
        self.mqtt_layout.addWidget(self.mqtt_port, 0, 3)

        self.mqtt_connect_button = QPushButton('Connect MQTT')
        self.mqtt_connect_button.clicked.connect(self.connect_mqtt)
        self.mqtt_layout.addWidget(self.mqtt_connect_button, 0, 4)

        # MQTT Message Section
        self.mqtt_topic_label = QLabel('MQTT Topic:')   
        self.mqtt_layout.addWidget(self.mqtt_topic_label, 1, 0)         
        self.mqtt_topic = QLineEdit()
        self.mqtt_layout.addWidget(self.mqtt_topic, 1, 1, 1, 2)   

        self.mqtt_message_label = QLabel('Message:')   
        self.mqtt_layout.addWidget(self.mqtt_message_label, 2, 0)         

        # Message input and buttons layout
        self.message_layout = QHBoxLayout()
        self.mqtt_layout.addLayout(self.message_layout, 2, 1, 1, 4)

        self.mqtt_message = QTextEdit()
        self.mqtt_message.setMaximumHeight(60)
        self.mqtt_message.setPlaceholderText("Enter your MQTT message here...")
        self.message_layout.addWidget(self.mqtt_message)

        # Buttons layout
        self.mqtt_buttons_layout = QVBoxLayout()
        self.message_layout.addLayout(self.mqtt_buttons_layout)

        self.mqtt_publish_button = QPushButton('Publish')
        self.mqtt_publish_button.clicked.connect(self.publish_mqtt)
        self.mqtt_buttons_layout.addWidget(self.mqtt_publish_button)

        self.mqtt_subscribe_button = QPushButton('Subscribe')
        self.mqtt_subscribe_button.clicked.connect(self.subscribe_mqtt)
        self.mqtt_buttons_layout.addWidget(self.mqtt_subscribe_button)

        self.clear_data_button = QPushButton('Clear Data')
        self.clear_data_button.clicked.connect(self.clear_data)
        self.mqtt_buttons_layout.addWidget(self.clear_data_button)

        # MQTT Data Display Section
        self.mqtt_data_label = QLabel('MQTT Data:')
        self.mqtt_layout.addWidget(self.mqtt_data_label, 3, 0, 1, 5)

        self.mqtt_data = QTextEdit()
        self.mqtt_layout.addWidget(self.mqtt_data, 4, 0, 1, 5)

        self.timestamp_checkboxes = QHBoxLayout()
        self.main_layout.addLayout(self.timestamp_checkboxes)

        self.show_mqtt_timestamp_checkbox = QCheckBox('Show MQTT Timestamp')
        self.show_mqtt_timestamp_checkbox.stateChanged.connect(self.toggle_show_mqtt_timestamp)
        self.timestamp_checkboxes.addWidget(self.show_mqtt_timestamp_checkbox)

        self.show_modbus_timestamp_checkbox = QCheckBox('Show Modbus Timestamp')
        self.show_modbus_timestamp_checkbox.stateChanged.connect(self.toggle_show_modbus_timestamp)
        self.timestamp_checkboxes.addWidget(self.show_modbus_timestamp_checkbox)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_data)
        self.timer.start(1000)  # Update every second

    def apply_styles(self):
        # Connection button style (Green theme)
        connection_style = """
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 2px 4px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 12px;
                margin: 2px;
                cursor: pointer;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """
        self.mqtt_connect_button.setStyleSheet(connection_style)

        # Read button style (Blue theme)
        read_style = """
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 2px 4px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 12px;
                margin: 2px;
                cursor: pointer;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #1565C0;
            }
        """
        self.modbus_read_button.setStyleSheet(read_style)

        # Publish button style (Orange theme)
        publish_style = """
            QPushButton {
                background-color: #FF9800;
                color: white;
                border: none;
                padding: 2px 4px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 12px;
                margin: 2px;
                cursor: pointer;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #F57C00;
            }
            QPushButton:pressed {
                background-color: #EF6C00;
            }
        """
        self.mqtt_publish_button.setStyleSheet(publish_style)

        # Subscribe button style (Purple theme)
        subscribe_style = """
            QPushButton {
                background-color: #9C27B0;
                color: white;
                border: none;
                padding: 2px 4px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 12px;
                margin: 2px;
                cursor: pointer;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #7B1FA2;
            }
            QPushButton:pressed {
                background-color: #6A1B9A;
            }
        """
        self.mqtt_subscribe_button.setStyleSheet(subscribe_style)


        # Clear button style (Red theme)
        clear_style = """
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                padding: 2px 4px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 12px;
                margin: 2px;
                cursor: pointer;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
            QPushButton:pressed {
                background-color: #c62828;
            }
        """
        # Only apply style to the clear_data_button since clear_message_button was removed
        self.clear_data_button.setStyleSheet(clear_style)

    def read_modbus(self):
        try:
            # Add your modbus read logic here
            message = "Reading from Modbus..."
            if self.show_modbus_timestamp:
                message = f"[{self.get_timestamp()}] {message}"
            self.modbus_data.append(message)
            QMessageBox.information(self, "Success", "Successfully read from Modbus device")
        except Exception as e:
            error_message = f"Modbus Read Error: {str(e)}"
            if self.show_modbus_timestamp:
                error_message = f"[{self.get_timestamp()}] {error_message}"
            self.modbus_data.append(error_message)
            QMessageBox.critical(self, "Error", f"Failed to read from Modbus: {str(e)}")

    def connect_mqtt(self):
        try:
            broker = self.mqtt_broker.text()
            port = int(self.mqtt_port.text())
            self.mqtt_handler.broker = broker
            self.mqtt_handler.port = port
            self.mqtt_handler.connect()
            message = f"Connected to MQTT broker at {broker}:{port}"
            if self.show_mqtt_timestamp:
                message = f"[{self.get_timestamp()}] {message}"
            self.mqtt_data.append(message)
            QMessageBox.information(self, "Success", f"Successfully connected to MQTT broker at {broker}:{port}")
        except Exception as e:
            error_message = f"MQTT Connection Error: {str(e)}"
            if self.show_mqtt_timestamp:
                error_message = f"[{self.get_timestamp()}] {error_message}"
            self.mqtt_data.append(error_message)
            QMessageBox.critical(self, "Error", f"Failed to connect to MQTT broker: {str(e)}")

    def clear_message(self):
        """Clear the MQTT message input field."""
        self.mqtt_message.clear()

    def clear_data(self):
        """Clear both MQTT and Modbus data displays."""
        self.mqtt_data.clear()
        self.modbus_data.clear()

    def publish_mqtt(self):
        try:
            topic = self.mqtt_topic.text()
            message = self.mqtt_message.toPlainText()  # Changed from text() to toPlainText()
            if not message:
                QMessageBox.warning(self, "Warning", "Message is empty, using default 'Test message'")
                message = "Test message"
            self.mqtt_handler.publish(topic, message)
            display_message = f"Published to {topic}: {message}"
            if self.show_mqtt_timestamp:
                display_message = f"[{self.get_timestamp()}] {display_message}"
            self.mqtt_data.append(display_message)
            QMessageBox.information(self, "Success", f"Successfully published message to topic: {topic}")
        except Exception as e:
            error_message = f"MQTT Publish Error: {str(e)}"
            if self.show_mqtt_timestamp:
                error_message = f"[{self.get_timestamp()}] {error_message}"
            self.mqtt_data.append(error_message)
            QMessageBox.critical(self, "Error", f"Failed to publish MQTT message: {str(e)}")

    def subscribe_mqtt(self):
        try:
            topic = self.mqtt_topic.text()
            if not topic:
                QMessageBox.warning(self, "Warning", "Please enter a topic to subscribe")
                return
            self.mqtt_handler.subscribe(topic)
            message = f"Subscribed to topic: {topic}"
            if self.show_mqtt_timestamp:
                message = f"[{self.get_timestamp()}] {message}"
            self.mqtt_data.append(message)
            QMessageBox.information(self, "Success", f"Successfully subscribed to topic: {topic}")
        except Exception as e:
            error_message = f"MQTT Subscribe Error: {str(e)}"
            if self.show_mqtt_timestamp:
                error_message = f"[{self.get_timestamp()}] {error_message}"
            self.mqtt_data.append(error_message)
            QMessageBox.critical(self, "Error", f"Failed to subscribe to topic: {str(e)}")

    def write_modbus(self):
        try:
            if not self.modbus_address.text() or not self.modbus_value.text():
                QMessageBox.warning(self, "Warning", "Please enter both address and value")
                return
            address = int(self.modbus_address.text())
            value = int(self.modbus_value.text())
            self.modbus_handler.write_data(address, value)
            message = f"Successfully wrote value {value} to register {address}"
            if self.show_modbus_timestamp:
                message = f"[{self.get_timestamp()}] {message}"
            self.modbus_data.append(message)
            QMessageBox.information(self, "Success", f"Successfully wrote value {value} to register {address}")
        except ValueError as e:
            error_message = "Invalid input: Please enter valid numbers for address and value"
            if self.show_modbus_timestamp:
                error_message = f"[{self.get_timestamp()}] {error_message}"
            self.modbus_data.append(error_message)
            QMessageBox.warning(self, "Input Error", error_message)
        except Exception as e:
            error_message = f"Write Error: {str(e)}"
            if self.show_modbus_timestamp:
                error_message = f"[{self.get_timestamp()}] {error_message}"
            self.modbus_data.append(error_message)
            QMessageBox.critical(self, "Error", f"Failed to write to Modbus: {str(e)}")

    def toggle_show_mqtt_timestamp(self, state):
        self.show_mqtt_timestamp = bool(state)

    def toggle_show_modbus_timestamp(self, state):
        self.show_modbus_timestamp = bool(state)

    def update_data(self):
        # Update MQTT messages if any
        try:
            for message in self.mqtt_handler.received_messages:
                display_message = f"Received: {message}"
                if self.show_mqtt_timestamp:
                    display_message = f"[{self.get_timestamp()}] {display_message}"
                self.mqtt_data.append(display_message)
            self.mqtt_handler.received_messages.clear()
        except Exception as e:
            print(f"Error updating MQTT messages: {e}")

    def get_timestamp(self):
        """Return current timestamp in a formatted string."""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]