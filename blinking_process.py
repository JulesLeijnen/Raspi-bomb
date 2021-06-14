from pause import until
import RPi.GPIO as gpio
import paho.mqtt.client as mqtt #import the client1
from time import sleep, time
import json
import logging

Blink_message_recieved = False
defused = False
blinkpin = 22
B_procces_inprogress = False

def on_messageBLink(client, userdata, message):
    global defused, B_procces_inprogress, blinkpin                               # B_procces_inprogress is a variable that makes sure the blinking sequence can only happen ones, and defused tells the blinker to stop.
    new_message = json.loads(str(message.payload.decode("utf-8")))
    print("BLINK: A message received")
    print("BLINK: message received in blinking_process.py: {}".format(new_message))
    if new_message[1] == "CLEARED" or new_message[1] == "BOOM":
        defused = True
        temp1 = json.dump(["B1", "Cleared 10-4"])
        client.publish("main_channel",temp1)
        sleep(2)
        gpio.cleanup()
        exit(0)
        

    if new_message[1] == "B" and not B_procces_inprogress:
        B_procces_inprogress = True
        until(new_message[4] + new_message[2] - new_message[3])
        print("BLINK: UNTILL over")
        currently_blinking = False
        while not defused:
            until(time() + 0.5)
            currently_blinking = not currently_blinking
            if currently_blinking and time() < new_message[4] + new_message[2]:
                gpio.output(blinkpin, gpio.HIGH)
            elif not currently_blinking and time() < new_message[4] + new_message[2]:
                gpio.output(blinkpin, gpio.LOW)
            elif time() > new_message[4] + new_message[2] + 1:
                defused = True
            pass
        for _ in range(10):
            gpio.output(blinkpin, gpio.HIGH)
            sleep(0.1)
            gpio.output(blinkpin, gpio.LOW)
            sleep(0.1)
            gpio.cleanup()
            exit(0)
            

def blinking_PRE_process(DEBUG):
    global defused, B_procces_inprogress, blinkpin
    broker_adress="192.168.178.15"
    client = mqtt.Client("B1") #create new instance
    client.on_message=on_messageBLink #attach function to callback
    client.connect(broker_adress) #connect to broker
    client.loop_start() #start the loop
    client.subscribe("main_channel")
    print("BLINK: Connected to broker on adress {} with name 'B1' and subscribed to 'main_channel'".format(broker_adress))
       

    #Setup GPIO stuff
    gpio.setmode(gpio.BOARD)
    gpio.setwarnings(DEBUG)
    gpio.setup(blinkpin, gpio.OUT)
    gpio.output(blinkpin, gpio.HIGH)
    sleep(0.1)
    gpio.output(blinkpin, gpio.LOW)
    sleep(0.1)

    while not defused:
        sleep(5)
    exit(0)



