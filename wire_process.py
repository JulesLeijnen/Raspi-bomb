from random import randrange, choice
import RPi.GPIO as gpio
import paho.mqtt.client as mqtt #import the client1
import json
import logging
from time import sleep

NOTCLEARED = True

def on_messageWires(client, userdata, message):
    global NOTCLEARED
    new_message = json.loads(str(message.payload.decode("utf-8")))
    print("WIRE: message received in wire_process.py: {}\nMessage topic={}\nMessage qos={}\nMessage retain flag={}\nMessage type={}\n".format(new_message, message.topic, message.qos, message.retain, type(message)))
    if new_message[1] == "CLEARED" or new_message[1] == "BOOM":
        NOTCLEARED = False
        sleep(2)
        gpio.cleanup()
        exit(0)


def Check_UI(wires, correct, DEBUG):
    global NOTCLEARED
    
    if DEBUG:
        logging.basicConfig(filename='logfile.log', level=logging.DEBUG, format='%(levelname)s: %(asctime)s: %(filename)s: %(funcName)s: \n\t%(message)s')
    if not DEBUG:
        logging.basicConfig(filename='logfile.log', level=logging.WARNING, format='%(levelname)s: %(asctime)s: %(filename)s: %(funcName)s: \n\t%(message)s')

    
    print("WIRE: Var's set: NOTCLEARED, {}; DEBUG, {}".format(NOTCLEARED, DEBUG))

    broker_address="192.168.178.15" 
    client = mqtt.Client("PWire") #create new instance
    print("WIRE: created new instance PWire")
    client.connect(broker_address) #connect to broker
    print("WIRE: Connected to broker")
    client.on_message=on_messageWires #attach function to callback
    client.subscribe("main_channel")
    dictionary = ["Module1", "R"]
    temp1 = json.dumps(dictionary)
    print("WIRE: Created a JSON dump of the register message")
    client.publish("main_channel",temp1)#publish
    print("WIRE: Published message R to the main channel")

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

    temp_list = ["Module1", "D"]
    MessageD = json.dumps(temp_list)
    temp_list2 = ["Module1", "D"]
    MessageF = json.dumps(temp_list2)

    while NOTCLEARED:
        if Wire_Cut_1 == 1 and  correct != 1 and wire_behandeld_1 == 0:
            wire_behandeld_1 = 1
            client.publish("main_channel",MessageF)                                 #Publish messageF to add 1 fault to the counter in main_process.py
        if Wire_Cut_2 == 1 and  correct != 2 and wire_behandeld_2 == 0:
            wire_behandeld_2 = 1
            client.publish("main_channel",MessageF)                                 #Publish messageF to add 1 fault to the counter in main_process.py
        if Wire_Cut_3 == 1 and  correct != 3 and wire_behandeld_3 == 0:
            wire_behandeld_3 = 1
            client.publish("main_channel",MessageF)                                 #Publish messageF to add 1 fault to the counter in main_process.py
        if Wire_Cut_4 == 1 and  correct != 4 and wire_behandeld_4 == 0:
            wire_behandeld_4 = 1
            client.publish("main_channel",MessageF)                                 #Publish messageF to add 1 fault to the counter in main_process.py
        if Wire_Cut_5 == 1 and  correct != 5 and wire_behandeld_5 == 0:
            wire_behandeld_5 = 1
            client.publish("main_channel",MessageF)                                 #Publish messageF to add 1 fault to the counter in main_process.py
        if Wire_Cut_6 == 1 and  correct != 6 and wire_behandeld_6 == 0:
            wire_behandeld_6 = 1
            client.publish("main_channel",MessageF)                                 #Publish messageF to add 1 fault to the counter in main_process.py

        if (Wire_Cut_1 == 1 and correct == 1) or (Wire_Cut_2 == 1 and correct == 2) or (Wire_Cut_3 == 1 and correct == 3) or (Wire_Cut_4 == 1 and correct == 4) or (Wire_Cut_5 == 1 and correct == 5) or (Wire_Cut_6 == 1 and correct == 6):
            client.publish("main_channel",MessageD)                                 #Publish messageD to remove 1 from the active_module counter in main_process.py
            NOTCLEARED = False
        pass
    gpio.cleanup()
    exit(0)
    return
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