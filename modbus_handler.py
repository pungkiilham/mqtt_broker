import minimalmodbus
import serial

class ModbusHandler:
    def __init__(self, com='COM1', baudrate=9600, timeout=1.0):
        self.com = com
        self.baudrate = baudrate
        self.timeout = timeout
        self.instrument = None

    def connect(self):
        """Connect to the Modbus device"""
        try:
            # Configure the instrument
            self.instrument = minimalmodbus.Instrument(self.com, 1)  # port name, slave address
            
            # Configure serial parameters
            self.instrument.serial.baudrate = self.baudrate
            self.instrument.serial.timeout = self.timeout
            self.instrument.serial.bytesize = 8
            self.instrument.serial.parity = serial.PARITY_NONE
            self.instrument.serial.stopbits = 1
            
            # Configure Modbus parameters
            self.instrument.mode = minimalmodbus.MODE_RTU
            self.instrument.clear_buffers_before_each_transaction = True
            
            return True
        except Exception as e:
            raise Exception(f"Failed to connect: {str(e)}")

    def disconnect(self):
        """Disconnect from the device"""
        if self.instrument:
            self.instrument.serial.close()
            self.instrument = None

    def read_data(self, address):
        """Read data from specified register"""
        try:
            if not self.instrument:
                raise Exception("Not connected to device")
            
            # Read the register (function code 0x03)
            value = self.instrument.read_register(address, 0)  # address, number of decimals
            return [value]
        except Exception as e:
            raise Exception(f"Failed to read register: {str(e)}")

    def write_data(self, address, value):
        """Write data to specified register"""
        try:
            if not self.instrument:
                raise Exception("Not connected to device")
            
            # Write to the register (function code 0x06)
            self.instrument.write_register(address, value, 0)  # address, value, number of decimals
        except Exception as e:
            raise Exception(f"Failed to write register: {str(e)}")