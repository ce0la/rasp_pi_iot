import RPi.GPIO as GPIO
import dht11
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from time import sleep
from datetime import date, datetime
 
# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
 
# AWS IoT certificate based connection
myMQTTClient = AWSIoTMQTTClient("123afhlss456")
myMQTTClient.configureEndpoint("a167lgi887r2fi-ats.iot.us-east-1.amazonaws.com", 8883)
myMQTTClient.configureCredentials("/home/pi/rasp_pi_iot/vars/CA.pem", "/home/pi/rasp_pi_iot/vars/6b1c526b1e-private.pem.key", "/home/pi/rasp_pi_iot/vars/6b1c526b1e-certificate.pem.crt")
myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
 
#connect and publish
myMQTTClient.connect()
myMQTTClient.publish("thing01/info", "connected", 0)
 
#loop and publish sensor reading

while 1:
    now = datetime.utcnow()
    now_str = now.strftime('%Y-%m-%dT%H:%M:%SZ') #e.g. 2016-04-18T06:12:25.877Z
    instance = dht11.DHT11(pin = 4) #BCM GPIO04
    result = instance.read()
    if result.is_valid():
        payload = '{ "timestamp": "' + now_str + '","temperature": ' + str(result.temperature) + ',"humidity": '+ str(result.humidity) + ' }'
        print payload
        myMQTTClient.publish("thing01/data", payload, 0)
        sleep(4)
    else:
        print (".")
        sleep(1)
