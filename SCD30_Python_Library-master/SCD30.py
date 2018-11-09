import smbus
import time
from converter import *

class Sensor:

    POLYNOMIAL = 0x31
    INITIALIZATION = 0xFF

    COMMAND_DATA_READY = 0x0202
    COMMAND_READ_MEASUREMENT = 0x0300

    def __init__(self, port=1, address=0x61):
        self.bus = smbus.SMBus(port)
        self.adr = address

    def readMeasurement(self):
##        if self.dataReady():

        data = self.readRegister(self.COMMAND_READ_MEASUREMENT, 18)
        co2m = data[0:3]
        co2l = data[3:6]
        tempm = data[6:9]
        templ = data[9:12]
        humm = data[12:15]
        huml = data[15:18]
        check = [self.verify(co2m), self.verify(co2l)]
        test = [self.mergeWord(co2m), self.mergeWord(co2l)]
        
        value = [0,0,0,0]
        
        value[0] = data[0]
        value[1] = data[1]
        value[2] = data[3]
        value[3] = data[4]
        Co2value = Converter.bytesToFloat(True,value)
        print("co2 value test:", Co2value)
        
        value[0] = data[6]
        value[1] = data[7]
        value[2] = data[9]
        value[3] = data[10]

        Tempvalue = Converter.bytesToFloat(True,value)
        print("temp value test:", Tempvalue)


        value[0] = data[12]
        value[1] = data[13]
        value[2] = data[15]
        value[3] = data[16]
        
        Humidvalue = Converter.bytesToFloat(True,value)
        print("humidity value test:", Humidvalue)
        
        return Co2value, Tempvalue, Humidvalue
##        
##        else:
##            print("Data not ready")

    def dataReady(self):
        data = self.readRegister(self.COMMAND_DATA_READY, 3)
        #print(data)
        ready = self.verify(data)
        return ready

    def sendCommand(self, cmd):  # sends a 2 byte command
        data = [0]*2
        data[0] = cmd >> 8
        data[1] = cmd & 0xFF
        self.bus.write_i2c_block_data(self.adr, data[0], data[1:])

    def readRegister(self, reg, length):
        self.sendCommand(reg)
        time.sleep(1)
        data = self.bus.read_i2c_block_data(self.adr, 0, length)
        return data

    def compareCRC8(self, data, crc):
        calc = self.calcCRC8(data)
        return calc == crc

    def mergeWord(self, data):
        return data[0] << 8 | data[1]

    def verify(self, data):
        value = data[0:2]
        crc = data[2]
        return crc == self.calcCRC8(value)

    def calcCRC8(self, data):
        crc = self.INITIALIZATION

        for byte in data:
            crc ^= byte
            for bit in range(8):
                if crc & 0x80:
                    crc = (crc << 1) ^ self.POLYNOMIAL
                else:
                    crc = (crc << 1)
                crc = crc % 256

        return crc
    
while True:
    s = Sensor()
    time.sleep(4)
##    s.dataReady()
    s.readMeasurement()
    
