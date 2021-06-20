from random import randrange, choice
import RPi.GPIO as gpio
import paho.mqtt.client as mqtt #import the client1
import json
import logging
from time import sleep

NOTCLEARED = True

MQTT_BROKER = "localhost"
MQTT_TOPIC_TO_MAIN = "to_main"
MQTT_TOPIC_FROM_MAIN = "from_main"
MQTT_QOS = 2
MQTT_RETAIN = True

def on_mqtt_messageWIRE(client, userdata, message):
    new_message = json.loads(str(message.payload.decode("utf-8")))
    print("WIRE: message received in wire_process.py: {}".format(new_message,))
    WireMessageResolver(new_message)

def WireMessageResolver(message):
    global NOTCLEARED
    if message[1] in ["Cleared", "BOOM"]:
        NOTCLEARED = False

def on_mqtt_connectWIRE(client, userdata, flags, rc):
    if (rc ==0):
        mqtt.Client.connected_flag = True
        print(">> on_mqtt_connectWIRE: mqtt broker connection OK")

        client.subscribe(MQTT_TOPIC_FROM_MAIN, MQTT_QOS)

    else:
        print(">> on_mqtt_connectWIRE: mqtt broker error: {}".format(rc))
        client.bad_connection_flag = True

def Wire_PubSubStuff():
    Wireclient = None
    mqtt.Client.connected_flag = False
    mqtt.Client.bad_connection_flag = False

    Wireclient = mqtt.Client("Wireclient")
    Wireclient.on_connect = on_mqtt_connectWIRE
    Wireclient.on_message = on_mqtt_messageWIRE

    try:
        Wireclient.connect(MQTT_BROKER)
        Wireclient.loop_start()
    except:
        print(">> Wire_PubSubStuff: Connection Failed")
    while not Wireclient.connected_flag and not Wireclient.bad_connection_flag:  #wait in loop
	    print(">> Wire_PubSubStuff(): in connection wait loop")
	    sleep(1)
    if Wireclient.bad_connection_flag:
        Wireclient.loop_stop()
        sleep(2)
        exit(0)
    return Wireclient

def Check_UI(wires, correct, DEBUG):
    global NOTCLEARED
    
    if DEBUG:
        logging.basicConfig(filename='logfile.log', level=logging.DEBUG, format='%(levelname)s: %(asctime)s: %(filename)s: %(funcName)s: \n\t%(message)s')
    if not DEBUG:
        logging.basicConfig(filename='logfile.log', level=logging.WARNING, format='%(levelname)s: %(asctime)s: %(filename)s: %(funcName)s: \n\t%(message)s')
    
    print("WIRE: Var's set: NOTCLEARED, {}; DEBUG, {}".format(NOTCLEARED, DEBUG))

#---------------------------------END_LOGGING/BEGIN_PUBSUB-----------------------------

    Wireclient = Wire_PubSubStuff()

    DoneArray = ["Wires1", "D"]
    DoneJSONdump = json.dumps(DoneArray)
    FaultArray = ["Wires1", "F"]
    FaultJSONdump = json.dumps(FaultArray)
    RegisterArray = ["Wires1", "R"]
    RegisterJSONdump = json.dumps(RegisterArray)

    Wireclient.publish(MQTT_TOPIC_TO_MAIN, RegisterJSONdump)

#----------------------------------END_PUBSUB/BEGIN_GPIO-------------------------------

    global DRAAD1, DRAAD2, DRAAD3, DRAAD4, DRAAD5, DRAAD6
    global Wire_Cut_1, Wire_Cut_2, Wire_Cut_3, Wire_Cut_4, Wire_Cut_5, Wire_Cut_6
    global wire_behandeld_1, wire_behandeld_2, wire_behandeld_3, wire_behandeld_4, wire_behandeld_5, wire_behandeld_6

    DRAAD1 = 7
    DRAAD2 = 13
    DRAAD3 = 15
    DRAAD4 = 8
    DRAAD5 = 10
    DRAAD6 = 11

    Wire_Cut_1 = 0
    Wire_Cut_2 = 0
    Wire_Cut_3 = 0
    Wire_Cut_4 = 0
    Wire_Cut_5 = 0
    Wire_Cut_6 = 0

    wire_behandeld_1 = 0
    wire_behandeld_2 = 0
    wire_behandeld_3 = 0
    wire_behandeld_4 = 0
    wire_behandeld_5 = 0
    wire_behandeld_6 = 0

    if not (DRAAD1 + DRAAD2 + DRAAD3 + DRAAD4 + DRAAD5 + DRAAD6) == 64 or not (Wire_Cut_1 + Wire_Cut_2 + Wire_Cut_3 + Wire_Cut_4 + Wire_Cut_5 + Wire_Cut_6 + wire_behandeld_1 + wire_behandeld_2 + wire_behandeld_3 + wire_behandeld_4 + wire_behandeld_5 + wire_behandeld_6) == 0:
        logging.error("Base variables have not been added correctly. This may couse glitches further in the program")
    else:
        print("WIRE: Wire variables created correctly in the wire process")

    gpio.setwarnings(DEBUG)
    gpio.setmode(gpio.BOARD)

    gpio.setup(DRAAD1, gpio.IN, pull_up_down=gpio.PUD_DOWN)
    gpio.setup(DRAAD2, gpio.IN, pull_up_down=gpio.PUD_DOWN)
    gpio.setup(DRAAD3, gpio.IN, pull_up_down=gpio.PUD_DOWN)

    gpio.add_event_detect(DRAAD1, gpio.FALLING, callback=CallbackD1)
    gpio.add_event_detect(DRAAD2, gpio.FALLING, callback=CallbackD2)
    gpio.add_event_detect(DRAAD3, gpio.FALLING, callback=CallbackD3)

    if len(wires) > 3:
        gpio.setup(DRAAD4, gpio.IN, pull_up_down=gpio.PUD_DOWN)
        gpio.add_event_detect(DRAAD4, gpio.FALLING, callback=CallbackD4)
    elif len(wires) > 4:
        gpio.setup(DRAAD5, gpio.IN, pull_up_down=gpio.PUD_DOWN)
        gpio.add_event_detect(DRAAD5, gpio.FALLING, callback=CallbackD5)
    elif len(wires) > 5:
        gpio.setup(DRAAD6, gpio.IN, pull_up_down=gpio.PUD_DOWN)
        gpio.add_event_detect(DRAAD6, gpio.FALLING, callback=CallbackD6)

    while NOTCLEARED:
        if Wire_Cut_1 == 1 and  correct != 1 and wire_behandeld_1 == 0:
            wire_behandeld_1 = 1
            Wireclient.publish(MQTT_TOPIC_TO_MAIN, FaultJSONdump)                                 #Publish messageF to add 1 fault to the counter in main_process.py
        if Wire_Cut_2 == 1 and  correct != 2 and wire_behandeld_2 == 0:
            wire_behandeld_2 = 1
            Wireclient.publish(MQTT_TOPIC_TO_MAIN, FaultJSONdump)
        if Wire_Cut_3 == 1 and  correct != 3 and wire_behandeld_3 == 0:
            wire_behandeld_3 = 1
            Wireclient.publish(MQTT_TOPIC_TO_MAIN, FaultJSONdump)
        if Wire_Cut_4 == 1 and  correct != 4 and wire_behandeld_4 == 0:
            wire_behandeld_4 = 1
            Wireclient.publish(MQTT_TOPIC_TO_MAIN, FaultJSONdump)   
        if Wire_Cut_5 == 1 and  correct != 5 and wire_behandeld_5 == 0:
            wire_behandeld_5 = 1
            Wireclient.publish(MQTT_TOPIC_TO_MAIN, FaultJSONdump)   
        if Wire_Cut_6 == 1 and  correct != 6 and wire_behandeld_6 == 0:
            wire_behandeld_6 = 1
            Wireclient.publish(MQTT_TOPIC_TO_MAIN, FaultJSONdump)   

        if (Wire_Cut_1 == 1 and correct == 1) or (Wire_Cut_2 == 1 and correct == 2) or (Wire_Cut_3 == 1 and correct == 3) or (Wire_Cut_4 == 1 and correct == 4) or (Wire_Cut_5 == 1 and correct == 5) or (Wire_Cut_6 == 1 and correct == 6):
            Wireclient.publish(MQTT_TOPIC_TO_MAIN, DoneJSONdump)   
            NOTCLEARED = False
        pass
    gpio.cleanup()
    exit(0)
#-------------------------------------------------------------------------------
def CallbackD1(channel):
    global Wire_Cut_1
    gpio.remove_event_detect(DRAAD1)
    print("WIRE: Draad 1 doorgeknipt")
    Wire_Cut_1 = 1
    return


def CallbackD2(channel):
    global Wire_Cut_2
    gpio.remove_event_detect(DRAAD2)
    print("WIRE: Draad 2 doorgeknipt")
    Wire_Cut_2 = 1
    return


def CallbackD3(channel):
    global Wire_Cut_3
    gpio.remove_event_detect(DRAAD3)
    print("WIRE: Draad 3 doorgeknipt")
    Wire_Cut_3 = 1
    return


def CallbackD4(channel):
    global Wire_Cut_4
    gpio.remove_event_detect(DRAAD4)
    print("WIRE: Draad 4 doorgeknipt")
    Wire_Cut_4 = 1
    return


def CallbackD5(channel):
    global Wire_Cut_5
    gpio.remove_event_detect(DRAAD5)
    print("WIRE: Draad 5 doorgeknipt")
    Wire_Cut_5 = 1
    return


def CallbackD6(channel):
    global Wire_Cut_6
    gpio.remove_event_detect(DRAAD6)
    print("WIRE: Draad 6 doorgeknipt")
    Wire_Cut_6 = 1
    return
#-------------------------------------------------------------------------------