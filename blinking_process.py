from pause import until
import RPi.GPIO as gpio
import paho.mqtt.client as mqtt #import the client1
from time import sleep, time
import json
import logging

Blink_message_recieved = False

def on_message(client, userdata, message):
    global defused, B_procces_inprogress                                # B_procces_inprogress is a variable that makes sure the blinking sequence can only happen ones, and defused tells the blinker to stop.
    new_message = json.loads(str(message.payload.decode("utf-8")))
    print("message received: {}\nMessage topic={}\nMessage qos={}\nMessage retain flag={}\nMessage type={}\n".format(new_message, message.topic, message.qos, message.retain, type(message)))
    if new_message[1] == "CLEARED":
        defused = True
    if new_message[1] == "B" and not B_procces_inprogress:
        B_procces_inprogress = True
        until(new_message[4] + new_message[2] - new_message[3])
        print("UNTILL over")
        currently_blinking = False
        while not defused:
            until(time() + 0.5)
            currently_blinking = not currently_blinking
            if currently_blinking:
                gpio.output(22, gpio.HIGH)
                print("HIGH")
            elif not currently_blinking:
                gpio.output(22, gpio.LOW)
                print("LOW")
            pass

def blinking_PRE_process(DEBUG):
    global defused, B_procces_inprogress
    defused = False
    broker_adress="192.168.178.15"
    client = mqtt.Client("B1") #create new instance
    client.on_message=on_message #attach function to callback
    client.connect(broker_adress) #connect to broker
    client.loop_start() #start the loop
    client.subscribe("main_channel")
    logging.info("Connected to broker on adress {} with name 'B1' and subscribed to 'main_channel'".format(broker_adress))
    
    B_procces_inprogress = False

    blinkpin = 22

    #Setup GPIO stuff
    gpio.setmode(gpio.BOARD)
    gpio.setwarnings(DEBUG)
    gpio.setup(blinkpin, gpio.OUT)

    while not defused:
        sleep(5)
    exit(0)

blinking_PRE_process(1)


