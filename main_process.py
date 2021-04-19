#TODO:
# Make a better wire_process.py
# Implement in timer_process.py that the function will send the message to start blinken from anywhere without repeating and taking to long
# Implement Logging in all processes (Main_process and MainV2 allready done.)
import logging
import paho.mqtt.client as mqtt #import the client
from time import sleep
import json
import RPi.GPIO as gpio
########################################

amount_mistakes = 0
active_Modules = 0
status = "Sleeping"
time_up = 0

logging.info("Var's set: amount_mistakes, {}; active_Modules, {}; status, {}; time_up, {}".format(amount_mistakes, active_Modules, status, time_up))

def on_message(client, userdata, message):
    global amount_mistakes, active_Modules, status, time_up
    logging.info("message received: " + str(message.payload.decode("utf-8")))
    logging.info("message topic={}".format(message.topic))
    logging.info("message qos={}".format(message.qos))
    logging.info("message retain flag={}".format(message.retain))
    logging.info("Message type = {}".format(type(message)))
    new_message = json.loads(str(message.payload.decode("utf-8")))
    logging.info(type(new_message))
    logging.info(new_message)
    logging.info(new_message[1])
    if new_message[1] == "R": #Register
        active_Modules += 1
        if status == "Sleeping":
            status = "Active"
    elif new_message[1] == "D": #Done
        active_Modules -= 1
    elif new_message[1] == "T": #Time up
        time_up = 1
    elif new_message[1] == "F": #Fault +1
        amount_mistakes += 1
    
    
########################################
def main_process(max_mistakes, DEBUG):
    global amount_mistakes, active_Modules, status, time_up
    if DEBUG:
        logging.basicConfig(filename='logfile.log', level=logging.DEBUG, format='%(levelname)s: %(asctime)s: %(filename)s: %(funcName)s: \n\t%(message)s')
    if not DEBUG:
        logging.basicConfig(filename='logfile.log', level=logging.WARNING, format='%(levelname)s: %(asctime)s: %(filename)s: %(funcName)s: \n\t%(message)s')

    broker_address="192.168.178.15"
    logging.info("creating new instance")
    client = mqtt.Client("P1") #create new instance
    logging.info("Created new instance of P1")
    client.on_message=on_message #attach function to callback
    logging.info("connecting to broker")
    client.connect(broker_address) #connect to broker
    logging.info("Conencted to broker")
    client.loop_start() #start the loop
    logging.info("Subscribing to topic,'main_channel'")
    client.subscribe("main_channel")
    while True:
        sleep(0.5)
        logging.info("amount_mistakes={}".format(amount_mistakes))
        logging.info("active_module={}".format(active_Modules))
        logging.info("status={}".format(status))
        logging.info("time_up={}".format(time_up))
        if status == "Active" and active_Modules < 1:
            logging.info("Entering the cleared loop")
            while True:
                logging.info("CLEARED")
                sleep(0.1)
                logging.info("amount_mistakes={}".format(amount_mistakes))
                logging.info("active_module={}".format(active_Modules))
                logging.info("status={}".format(status))
                logging.info("time_up={}".format(time_up))
                sleep(0.5)
        pass
        if amount_mistakes > (max_mistakes - 1) or time_up == 1:
            logging.info("Entering the Boom loop")
            while True:
                logging.info("BOOM!")
                logging.info("BOOM!")
                logging.info("BOOM!")
                gpio.cleanup()
                sleep(0.1)
                logging.info("amount_mistakes={}".format(amount_mistakes))
                logging.info("active_module={}".format(active_Modules))
                logging.info("status={}".format(status))
                logging.info("time_up={}".format(time_up))
                logging.info("")
                logging.info("")
                logging.info("")
                sleep(0.5)
    client.loop_stop() #stop the loop