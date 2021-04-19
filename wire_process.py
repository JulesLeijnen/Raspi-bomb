from random import randrange, choice
import RPi.GPIO as gpio
import paho.mqtt.client as mqtt #import the client1
import json



def Check_UI(wires, correct):
    global NOTCLEARED, WINSTATUS
    WINSTATUS = 0
    NOTCLEARED = True
    DEBUG = 1

    broker_address="192.168.178.15" 
    client = mqtt.Client("PWire") #create new instance
    client.connect(broker_address) #connect to broker

    dictionary = ["Module1", "R"]
    temp1 = json.dumps(dictionary)
    client.publish("main_channel",temp1)#publish

    global DRAAD1, DRAAD2, DRAAD3, DRAAD4, DRAAD5, DRAAD6
    global Wire_Cut_1, Wire_Cut_2, Wire_Cut_3, Wire_Cut_4, Wire_Cut_5, Wire_Cut_6
    global wire_behandeld_1, wire_behandeld_2, wire_behandeld_3, wire_behandeld_4, wire_behandeld_5, wire_behandeld_6

    DRAAD1 = 7
    DRAAD2 = 13
    DRAAD3 = 15
    DRAAD4 = 8
    DRAAD5 = 10
    DRAAD6 = 12

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
            dictionary = ["Module1", "F"]
            temp1 = json.dumps(dictionary)
            client.publish("main_channel",temp1)#publish
        if Wire_Cut_2 == 1 and  correct != 2 and wire_behandeld_2 == 0:
            wire_behandeld_2 = 1
            dictionary = ["Module1", "F"]
            temp1 = json.dumps(dictionary)
            client.publish("main_channel",temp1)#publish
        if Wire_Cut_3 == 1 and  correct != 3 and wire_behandeld_3 == 0:
            wire_behandeld_3 = 1
            dictionary = ["Module1", "F"]
            temp1 = json.dumps(dictionary)
            client.publish("main_channel",temp1)#publish
        if Wire_Cut_4 == 1 and  correct != 4 and wire_behandeld_4 == 0:
            wire_behandeld_4 = 1
            dictionary = ["Module1", "F"]
            temp1 = json.dumps(dictionary)
            client.publish("main_channel",temp1)#publish
        if Wire_Cut_5 == 1 and  correct != 5 and wire_behandeld_5 == 0:
            wire_behandeld_5 = 1
            dictionary = ["Module1", "F"]
            temp1 = json.dumps(dictionary)
            client.publish("main_channel",temp1)#publish
        if Wire_Cut_6 == 1 and  correct != 6 and wire_behandeld_6 == 0:
            wire_behandeld_6 = 1
            dictionary = ["Module1", "F"]
            temp1 = json.dumps(dictionary)
            client.publish("main_channel",temp1)#publish

        if Wire_Cut_1 == 1 and correct == 1:
            temp_list = ["Module1", "D"]
            temp1 = json.dumps(temp_list)
            client.publish("main_channel",temp1)#publish
            NOTCLEARED = False
        if Wire_Cut_2 == 1 and correct == 2:
            temp_list = ["Module1", "D"]
            temp1 = json.dumps(temp_list)
            client.publish("main_channel",temp1)#publish
            NOTCLEARED = False
        if Wire_Cut_3 == 1 and correct == 3:
            temp_list = ["Module1", "D"]
            temp1 = json.dumps(temp_list)
            client.publish("main_channel",temp1)#publish
            NOTCLEARED = False
        if Wire_Cut_4 == 1 and correct == 4:
            temp_list = ["Module1", "D"]
            temp1 = json.dumps(temp_list)
            client.publish("main_channel",temp1)#publish
            NOTCLEARED = False
        if Wire_Cut_5 == 1 and correct == 5:
            temp_list = ["Module1", "D"]
            temp1 = json.dumps(temp_list)
            client.publish("main_channel",temp1)#publish
            NOTCLEARED = False
        if Wire_Cut_6 == 1 and correct == 6:
            temp_list = ["Module1", "D"]
            temp1 = json.dumps(temp_list)
            client.publish("main_channel",temp1)#publish
            NOTCLEARED = False
        

        if WINSTATUS == 1:
            print("Win!!")
            temp_list = ["Module1", "D"]
            temp1 = json.dumps(temp_list)
            client.publish("main_channel",temp1)#publish
            NOTCLEARED = False
        pass
    gpio.cleanup()
#-------------------------------------------------------------------------------
def CallbackD1(channel):
    global Wire_Cut_1
    gpio.remove_event_detect(DRAAD1)
    print("Draad 1 doorgeknipt")
    Wire_Cut_1 = 1
    return


def CallbackD2(channel):
    global Wire_Cut_2
    gpio.remove_event_detect(DRAAD2)
    print("Draad 2 doorgeknipt")
    Wire_Cut_2 = 1
    return


def CallbackD3(channel):
    global Wire_Cut_3
    gpio.remove_event_detect(DRAAD3)
    print("Draad 3 doorgeknipt")
    Wire_Cut_3 = 1
    return


def CallbackD4(channel):
    global Wire_Cut_4
    gpio.remove_event_detect(DRAAD4)
    print("Draad 4 doorgeknipt")
    Wire_Cut_4 = 1
    return


def CallbackD5(channel):
    global Wire_Cut_5
    gpio.remove_event_detect(DRAAD5)
    print("Draad 5 doorgeknipt")
    Wire_Cut_5 = 1
    return


def CallbackD6(channel):
    global Wire_Cut_6
    gpio.remove_event_detect(DRAAD6)
    print("Draad 6 doorgeknipt")
    Wire_Cut_6 = 1
    return
#-------------------------------------------------------------------------------