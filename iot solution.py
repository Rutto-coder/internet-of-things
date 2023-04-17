
#Import the necessary libraries 
import RPi.GPIO as GPIO 
import sys
import urllib.request as urllib2
from time import sleep
import Adafruit_DHT as dht
from machine import Pin, PWM
# Enter Your API key here
myAPI = '7NAPZ0CLX18B4R50' 

# URL where we will send the data, Don't change it
baseURL = 'https://api.thingspeak.com/update?api_key=%s' % myAPI 

#Set up the General purpose input output (GPIO) pins
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN)     #set the PIR input pin
GPIO.setup(8, GPIO.IN)     #set the LDR input pin
GPIO.setup(10, GPIO.OUT)   #set up the LDR LED
GPIO.setup(9, GPIO.OUT)     #set up the PIR LED        

Motion_message = ''

while True:
	i=GPIO.input(11)                  #Read output from PIR motion sensor
	if i==0:                        #When output from motion sensor is LOW
		Motion_message = "No Pedestrians"
		GPIO.output(9,False)
		time.sleep(0.1)

	elif i==1:                             #When output from motion sensor is HIGH
	Motion_message = "Pedestrians crossing"
	GPIO.output(9,True)
	buzzer = PWM(Pin(1))
	buzzer.freq(500)
	buzzer.duty_u16(1000)
	sleep(1)
	buzzer.duty_u16(0)
	time.sleep(0.1)


	if  GPIO.input(8) == 1:
		print('Low light turning on the headlights')
		GPIO.output(10,True)            #Turn on the LED

	else:
		print('Low light over turning of the headlights')
		GPIO.output(10,False)   



def read_data():
	# Reading from DHT22 and storing the temperature and humidity
	humi, temp = dht.read_retry(dht.DHT22, 7) 
	return humi, temp

while True:
	try:
		humi, temp = read_data()

		# If Reading is valid
		if isinstance(humi, float) and isinstance(temp, float):
			# Formatting to two decimal places
			humi = '%.2f' % humi 					   
			temp = '%.2f' % temp
			
			# Send the data to thingspeak
			conn = urllib2.urlopen(baseURL + '&field1=%s&field2=%s&field3' % (temp, humi, Motion_message))
			print(conn.read())
			# Close the connection
			conn.close()
		else:
			print('Error')
		# DHT22 requires 2 seconds to give a reading, so make sure to add delay of above 2 seconds.
		sleep(20)
	except:
		break