# Sample code for ESP8266 & ESP32, Micropython.org firmware
from machine import I2C, Pin, unique_id
from libs.ads1115 import ADS1115
from libs.sensor import ADC
from time import sleep_ms, ticks_ms, ticks_us, localtime
from array import array
from math import sqrt
from config import *
import ubinascii 
import _thread
from libs.mqtt import MQTTClient
import libs.webserver as ws
import network

print("=== Starting main script ===")

LAST_ACTIVATION = "NaN"
lock_last_activate = _thread.allocate_lock()

plateau_count = 0
plateau_min_point = None
platue_scan = False

# Callback Function to respond to messages from Adafruit IO
def sub_cb(topic, msg):          # sub_cb means "callback subroutine"
    print((topic, msg))          # Outputs the message that was received. Debugging use.
    if msg == b"ON":             # If message says "ON" ...
        print("ON")       # ... then LED on
    elif msg == b"OFF":          # If message says "OFF" ...
        print("OFF")                # ... then LED off
    else:                        # If any other message is received ...
        print("Unknown message") # ... do nothing but output that it happened.


def send(power,mqtt_client,topic):
    print("Publishing: {0} to {1} ... ".format(power, topic), end='')
    try:
        mqtt_client.publish(topic=topic, msg=str(power))
        print("DONE")
    except Exception as e:
        print("FAILED TO PUBLISH WITH MQTT")

def find_plateau(current_value,last_value):
    global plateau_count
    global platue_scan
    global plateau_min_point

    if platue_scan:
        if abs(current_value - plateau_min_point) >= PLATEAU_THRESHOLD:
            plateau_count +=1
        else:
            plateau_count = 0
            platue_scan = False
        
        if plateau_count >= PLATEAU_COUNT_THRESHOLD:
            platue_scan = False
            return True
        return False
    else:   
        if (current_value - last_value >= PLATEAU_THRESHOLD):
            plateau_min_point = last_value
            platue_scan = True
        return False
    
def web_thread(ip):
    global LAST_ACTIVATION
    try:
        connection = ws.open_socket(ip)
        ws.serve(connection,LAST_ACTIVATION)
    except KeyboardInterrupt:
        raise(KeyboardInterrupt)

        

#ip = network.WLAN(network.STA_IF).ifconfig()[0]
#_thread.start_new_thread(web_thread,(ip,))

i2c = I2C(1, scl=Pin(15), sda=Pin(14))

#YMDC clamps 4.096 100 amp 
YMDC_ADS = ADS1115(i2c,address=72, gain=1)
YMDC1 = ADC(YMDC_ADS,30,1,0,1)


AIO_CLIENT_ID = ubinascii.hexlify(unique_id())
mqtt_client = MQTTClient(AIO_CLIENT_ID,AIO_SERVER,AIO_PORT,AIO_USER,AIO_KEY)

mqtt_client.set_callback(sub_cb)
mqtt_client.connect()
mqtt_client.subscribe(MQTT_TOGGLE_MEASURMENT)
print("Connected to %s, subscribed to %s topic" % (AIO_SERVER, MQTT_TOGGLE_MEASURMENT))


try:
    YMDC1.read()
    power = YMDC1.getAmps(SYSTEM_VOLTAGE)
    power_last = 0

    while(1):
        print("=== ADC reading ===")
        YMDC1.read()
        power_last = power
        power = YMDC1.getAmps(SYSTEM_VOLTAGE)

        print("===== MQTT =====")
        mqtt_client.check_msg()
        send(power, mqtt_client,MQTT_POWER_MEASURMENTS)
        print("===================")

        found_platue = find_plateau(power,power_last)
        print("=== Plateau ===")
        print("scan: " + str(platue_scan))
        if platue_scan: print("count = " +str(plateau_count))
        print("found: " + str(found_platue))
        print("===============")
        if found_platue:
            year,month,day,hour,minute,_,_,_ = localtime()
            msg = f"The last power-on ocurred {hour:02}:{minute:02} {day}/{month}/{year}"
            #with lock_last_activate:
            LAST_ACTIVATION = msg
            print(msg)
            send(msg,mqtt_client,MQTT_LAST_TURN_ON)
        sleep_ms(7000)
finally:
    mqtt_client.disconnect
    mqtt_client = None
    Pin("LED",Pin.OUT).off
    print("=== Finishing main script ===")
