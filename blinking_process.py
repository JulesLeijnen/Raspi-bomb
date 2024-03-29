#--------------------------------------Imports---------------------------------------
from pause import until
import logging
import paho.mqtt.client as mqtt #import the client1
import json
from time import sleep, time
import RPi.GPIO as gpio
#--------------------------------------Globals--------------------------------------
MQTT_BROKER = "localhost"
MQTT_TOPIC_TO_MAIN = "to_main"
MQTT_TOPIC_FROM_MAIN = "from_main"
MQTT_QOS = 2
MQTT_RETAIN = True
#------------------------------------Main Function---------------------------------------
def Blinker_Process(DEBUG):
    global DEBUGStatus, blinkpin, start_blinking_peramiters, bomb_done_blinker, blinkpin
    
    DEBUGStatus = DEBUG
    bomb_done_blinker = False
    start_blinking_peramiters = []
    wait_var = 0

    #Loggingstuff

    Blinkerclient = Blinker_PubSubStuff()

    gpio_blinker_setup()

    while not len(start_blinking_peramiters) == 5:
        print(start_blinking_peramiters)
        sleep(0.1)
        wait_var += 1
        if wait_var % 25 == 0:
            print("Waiting for the blinking info")
    
    print(time())
    print(float(start_blinking_peramiters[4] + (start_blinking_peramiters[2] - start_blinking_peramiters[3])))
    until(float(start_blinking_peramiters[4] + (start_blinking_peramiters[2] - start_blinking_peramiters[3])))
    
    stoptime = time() + start_blinking_peramiters[3]
    while time() < stoptime and not bomb_done_blinker:
        sleep(0.5)
        gpio.output(blinkpin,gpio.HIGH)
        sleep(0.5)
        gpio.output(blinkpin,gpio.LOW)
    gpio.cleanup()
    sleep(2)
    exit(0)

#----------------------------------------LOGGING------------------------------------------

#------------------------------------MQTT Functions---------------------------------------
def Blinker_PubSubStuff():
    Blinkerclient = None
    mqtt.Client.connected_flag = False
    mqtt.Client.bad_connection_flag = False

    Blinkerclient = mqtt.Client("Blinkerclient")
    Blinkerclient.on_connect = on_mqtt_connectBLINKER
    Blinkerclient.on_message = on_mqtt_messageBLINKER

    try:
        Blinkerclient.connect(MQTT_BROKER)
        Blinkerclient.loop_start()
    except:
        print(">> Blinker_PubSubStuff: Connection Failed")
    while not Blinkerclient.connected_flag and not Blinkerclient.bad_connection_flag:  #wait in loop
	    print(">> Blinker_PubSubStuff: in connection wait loop")
	    sleep(1)
    if Blinkerclient.bad_connection_flag:
        Blinkerclient.loop_stop()
        sleep(2)
        exit(0)
    return Blinkerclient

def on_mqtt_connectBLINKER(client, userdata, flags, rc):
    if (rc ==0):
        mqtt.Client.connected_flag = True
        print(">> on_mqtt_connectBLINKER: mqtt broker connection OK")
        client.subscribe(MQTT_TOPIC_FROM_MAIN, MQTT_QOS)
    else:
        print(">> on_mqtt_connectBLINKER: mqtt broker error: {}".format(rc))
        client.bad_connection_flag = True
    return

def on_mqtt_messageBLINKER(client, userdata, message):
    new_message = json.loads(str(message.payload.decode("utf-8")))
    print("BLINKER: message received in timer_process.py: {}".format(new_message,))
    BlinkerMessageResolver(new_message)
    return

def BlinkerMessageResolver(message):
    global start_blinking_peramiters
    if len(message) == 5:
        start_blinking_peramiters = message
        print("TEMP22")
    else:
        print("TEMP33")
        print('\nType is {}, message is {}\n\n'.format(type(message), message))
        pass
    return

#----------------------------GPIO Stuff---------------------------
def gpio_blinker_setup():
    global DEBUGStatus, blinkpin

    blinkpin = 22

    gpio.setmode(gpio.BOARD)
    gpio.setwarnings(DEBUGStatus)
    gpio.setup(blinkpin, gpio.OUT)
    return