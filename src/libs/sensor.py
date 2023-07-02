from time import sleep_ms
from math import sqrt
########ADC Reads#########
ADC_RATE = 3 # delay rate in milliseconds

class ADC:
    def __init__(self, ADS,maxCurrent,maxVoltage, channel1, channel2 = None):
        self.ADS = ADS
        self.maxCurrent = maxCurrent
        self.maxVoltage = maxVoltage
        self.readTotal = 0
        self.readCount = 0
        self.channel1 = channel1
        self.channel2 = channel2
    
    def read(self):       
        self.ADS.set_conv(7,self.channel1, self.channel2)
        
        for x in range(0, 120):
            sleep_ms(ADC_RATE)
            self.readTotal += self.ADS.read_rev() ** 2.0
            self.readCount +=1
        
    def getAmps(self, system_voltage):
        sensor_output_voltage = self.ADS.raw_to_v(sqrt(self.readTotal/ self.readCount ))
        current = (self.maxCurrent / self.maxVoltage) * sensor_output_voltage 
        power = current * system_voltage
        #print("voltage " + str(voltage))
        print("current " + str(current))
        print("Watts: "+ str(power))
        self.readTotal = 0
        self.readCount = 0
        return power