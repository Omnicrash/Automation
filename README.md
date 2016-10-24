# Automation
A collection of home automation scripts

# sensors.py
A simple script that measures the temperature and relative humidity, displays it on two seven segment displays, and sends the data to a virtual sensor on a system running Domoticz.

The ```minTemp```, ```maxTemp```, ```minHum``` and ```maxHum``` values will cause their respective displays to blink whenever they are exceeded.

Change the server address (if Domoticz is not running locally or on a different port), the username and the password accordingly. Authentication in Domoticz might have to be set to Basic-Auth.

```
server = "127.0.0.1:8080"
user = "USERNAME"
password = "PASSWORD"
```

To change the pin the DHT22 is connected on, change ```dhtPin = 4``` to the appropriate pin.  
The ID of the virtual weather sensor needs to be changed in the following line: ```dhtIDX = 32```.

By default the temperature lcd backpack is set to address 0x70 and the humidity lcd backpack is set to 0x71.

Requires the following libraries:  
https://github.com/adafruit/Adafruit_Python_DHT  
https://github.com/adafruit/Adafruit_Python_LED_Backpack  
