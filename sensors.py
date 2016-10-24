#!/usr/bin/env python

# Temp/Humidity display
# 2016 Yve Verstrepen

import time, urllib2, json, base64

import Adafruit_DHT
from Adafruit_LED_Backpack import SevenSegment, HT16K33

# Domoticz server
# Change these values for your setup
server = "127.0.0.1:8080"
user = "USERNAME"
password = "PASSWORD"
base64auth = base64.encodestring('%s:%s' % (user, password)).replace('\n', '')

# DHT22
dhtPin = 4
dhtIDX = 32 # Domoticz virtual sensor
dhtURL  = 'http://'+server+'/json.htm?type=command&param=udevice&idx='+str(dhtIDX)+'&nvalue=0&svalue='

# Display characters
lcd_P = 0x73
lcd_W1 = 0x3C
lcd_W2 = 0x1E
lcd_R = 0x33

lcd_O = 0x3F
lcd_N = 0x37

lcd_C = 0x39
lcd_H = 0x76

tempLCD = SevenSegment.SevenSegment(address=0x70)
rhLCD = SevenSegment.SevenSegment(address=0x71)

# When these values are exceeded, the display(s) will blink
minTemp = 18.0
maxTemp = 24.0
minHum = 40.0
maxHum = 60.0

def calc_hum_stat(humidity):
    hum_stat = 2 # Dry
    if humidity >= minHum and humidity < maxHum: hum_stat = 0 # Normal
    elif humidity >= maxHum: hum_stat = 3 # Wet
    return hum_stat

def domoticz_post(url):
    request = urllib2.Request(url)
    request.add_header("Authorization", "Basic %s" % base64auth)
    response = urllib2.urlopen(request)
    return response.read()

def display_value(display, value, ext):
    display.clear()
    decimals = 1
    if value >= 99.95 or value <= -9.95:
        decimals = 0
    display.print_float(value, decimal_digits=decimals, justify_right=False)
    display.set_digit_raw(3, ext)
    display.write_display()


# Initialize displays
# I use a green display for temperature and a blue one for humidity,
# brightness values below are tweaked so they appear similar in intensity. Adjust according to your setup.
tempLCD.begin()
tempLCD.set_brightness(12)
rhLCD.begin()
rhLCD.set_brightness(4)

# Show boot logo (PWR ON)
tempLCD.clear()
rhLCD.clear()

tempLCD.set_digit_raw(0, lcd_P)
tempLCD.set_digit_raw(1, lcd_W1)
tempLCD.set_digit_raw(2, lcd_W2)
tempLCD.set_digit_raw(3, lcd_R)

#rhLCD.set_digit_raw(0, lcd_O)
rhLCD.set_digit_raw(1, lcd_O)
rhLCD.set_digit_raw(2, lcd_N)
#rhLCD.set_digit_raw(3, lcd_O)

tempLCD.write_display()
rhLCD.write_display()

time.sleep(3.0)

# Continuously monitor temp & relative humidity, and update displays
print('Temperature & humidity monitoring started.')
while True:
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, dhtPin)
    if humidity is not None and temperature is not None:
        #print('Temp={0:0.1f}C  Humidity={1:0.1f}%RH'.format(temperature, humidity))
        hum_stat = calc_hum_stat(humidity)
        url = dhtURL+'{0:.2f}'.format(temperature)+';'+'{0:.2f}'.format(humidity)+';'+str(hum_stat)
        #print(url)
        domoticz_post(url)
        display_value(tempLCD, temperature, lcd_C)
        display_value(rhLCD, humidity, lcd_H)
        
        # Blink displays if it gets too cold/hot/dry/wet
        if temperature < minTemp or temperature >= maxTemp:
            tempLCD.set_blink(HT16K33.HT16K33_BLINK_1HZ)
        else:
            tempLCD.set_blink(HT16K33.HT16K33_BLINK_OFF)
        
        if humidity < minHum or humidity >= maxHum:
            rhLCD.set_blink(HT16K33.HT16K33_BLINK_1HZ)
        else:
            rhLCD.set_blink(HT16K33.HT16K33_BLINK_OFF)
        
    time.sleep(1.0)
