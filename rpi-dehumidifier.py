import time
import lcddriver
import RPi.GPIO as GPIO
from Adafruit_BME280 import BME280, BME280_OSAMPLE_8

RELAY_PIN = 21
LIMIT = 60

try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RELAY_PIN, GPIO.OUT)

    lcd = lcddriver.lcd()

    while True:
        sensor = BME280(mode=BME280_OSAMPLE_8)

        degrees = sensor.read_temperature()
        pascals = sensor.read_pressure()
        hectopascals = pascals / 100
        humidity = sensor.read_humidity()

        print 'Timestamp = {0:0.3f}'.format(sensor.t_fine)
        print 'Temp      = {0:0.3f} deg C'.format(degrees)
        print 'Pressure  = {0:0.2f} hPa'.format(hectopascals)
        print 'Humidity  = {0:0.2f} %'.format(humidity)

        lcd.lcd_clear()
        lcd.lcd_display_string('Humidity:', 1)
        lcd.lcd_display_string('{0:0.2f}%'.format(humidity), 2)

        if humidity > LIMIT:
            GPIO.output(RELAY_PIN, GPIO.LOW)
        else:
            GPIO.output(RELAY_PIN, GPIO.HIGH)

        time.sleep(3)
except KeyboardInterrupt:
    GPIO.cleanup()

