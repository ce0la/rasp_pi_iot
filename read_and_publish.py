import os
import json
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
myMQTTClient.configureCredentials("/home/pi/rasp_pi_iot/certificates/root.pem", "/home/pi/rasp_pi_iot/certificates/d8f0107328-private.pem.key", "/home/pi/rasp_pi_iot/certificates/d8f0107328-certificate.pem.crt")
myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

#connect and publish
myMQTTClient.connect()
print("Connected to AWS IoT")
myMQTTClient.publish("test/testing", "connected", 0)

#loop and publish sensor reading

while 1:
    now = datetime.utcnow()
    now_str = now.strftime('%Y-%m-%dT%H:%M:%SZ') #e.g. 2016-04-18T06:12:25.877Z
    #instance = dht11.DHT11(pin = 4) #BCM GPIO04
    temp = os.system("vcgencmd measure_temp | egrep -o '[0-9]*\.[0-9]*'")
    data = str(temp)
    #result = instance.read()
    #if result.is_valid():
    if True:
#        payload = '{ "timestamp": "' + now_str + '","temperature": ' + str(data) + ' }'
        payload = {"timestamp" : now_str, "temperature" : data}
        print(payload)
        myMQTTClient.publish("test/testing", json.dumps(payload), 1)
        print("Published: '" + str(payload) + "' to the topic: " + "'test/testing'")
        sleep(4)
    else:
        print ("Something is not right somewhere")
        sleep(1)
