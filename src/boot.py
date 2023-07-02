# boot.py -- run on boot-up
import network
from time import sleep,gmtime
from config import WIFI_SSID,WIFI_PASSWORD,GM_OFFSET,NTP_SERVER,DAYLIGHT_SAVING
from machine import Pin, RTC
import socket
import struct

NTP_DELTA = 2208988800 - GM_OFFSET * 3600 - DAYLIGHT_SAVING * 3600

def set_time():
    NTP_QUERY = bytearray(48)
    NTP_QUERY[0] = 0x1B
    addr = socket.getaddrinfo(NTP_SERVER, 123)[0][-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.settimeout(10)
        res = s.sendto(NTP_QUERY, addr)
        msg = s.recv(48)
    finally:
        s.close()
    val = struct.unpack("!I", msg[40:44])[0]
    t = val - NTP_DELTA    
    tm = gmtime(t)
    RTC().datetime((tm[0], tm[1], tm[2], tm[6] + 1, tm[3], tm[4], tm[5], 0))


def do_connect():

    print("==== Run Boot script === ")
    wlan = network.WLAN(network.STA_IF)         # Put modem on Station mode

    if not wlan.isconnected():                  # Check if already connected
        print('connecting to network...')
        wlan.active(True)                       # Activate network interface
        # set power mode to get WiFi power-saving off (if needed)
        wlan.config(pm = 0xa11140)
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)  # Your WiFi Credential
        print('Waiting for connection...', end='')
        # Check if it is connected otherwise wait
        while not wlan.isconnected() and wlan.status() >= 0:
            print('.', end='')
            sleep(1)
    # Print the IP assigned by router
    ip = wlan.ifconfig()[0]
    print('\nConnected on {}'.format(ip))
    return ip 

Pin("LED",Pin.OUT).on()

# WiFi Connection
try:
    ip = do_connect()
    #set_time()
except KeyboardInterrupt:
    print("Keyboard interrupt")

print("=== Done with boot script ===")