#TODO:
# Make a better wire_process.py
# Implement a stop from message (MQTT) in wire_process.py
# Implement in timer_process.py that the function will send the message to start blinken from anywhere without repeating and taking to long
# Implement Logging in all processes (Main_process and MainV2 allready done.)
# Clean up Imports
import logging
import paho.mqtt.client as mqtt                             #import the client needed fot the MQTT broker
from time import sleep
import json                                                 #Imports JSON to convert arrays to strings and back
from sys import exit
import RPi.GPIO as gpio                                     #Imports the GPIO lib to control the GPIO pins
########################################

#These are all the variables that the main process needs to keep track of
amount_mistakes = 0
active_Modules = 0
status = "Sleeping"
time_up = 0

logging.info("Var's set: amount_mistakes, {}; active_Modules, {}; status, {}; time_up, {}".format(amount_mistakes, active_Modules, status, time_up))

########################################

def on_message(client, userdata, message):
    global amount_mistakes, active_Modules, status, time_up
    new_message = json.loads(str(message.payload.decode("utf-8")))
    logging.info("message received: {}\nMessage topic={}\nMessage qos={}\nMessage retain flag={}\nMessage type={}\n".format(new_message, message.topic, message.qos, message.retain, type(message)))
    if new_message[1] == "R": #Register
        active_Modules += 1
        if status == "Sleeping":
            status = "Active"
            logging.info("Changing status from 'Sleeping' to 'Active' And added 1 to active_Modules")
        else:
            logging.info("Added 1 to active_Modules, current total is {}".format(active_Modules))
    elif new_message[1] == "D": #Done
        active_Modules -= 1
        logging.info("Removed 1 from active_Modules, current total is {}".format(active_Modules))
    elif new_message[1] == "T": #Time up
        time_up = 1
        logging.info("Time is up, current state is '{}'".format(bool(time_up)))
    elif new_message[1] == "F": #Fault +1
        amount_mistakes += 1
        logging.info("Added 1 to amount_mistakes, current total is {}".format(amount_mistakes))
        
########################################

def main_process(max_mistakes):
    global amount_mistakes, active_Modules, status, time_up

    broker_adress="192.168.178.15"
    client = mqtt.Client("P1") #create new instance
    client.on_message=on_message #attach function to callback
    client.connect(broker_adress) #connect to broker
    client.loop_start() #start the loop
    client.subscribe("main_channel")
    logging.info("Connected to broker on adress {} with name 'P1' and subscribed to 'main_channel'".format(broker_adress))
    while True:
        sleep(0.5)
        if status == "Active" and active_Modules < 1:
            #SEND MESSAGE TO REST OF BOMB
            logging.info("Entered the cleared loop")
            logging.info("CLEARED\n\namount_mistakes={}\nactive_module={}\nstatus={}\ntime_up={}\n".format(amount_mistakes, active_Modules, status, time_up))
            gpio.cleanup()
            exit(0)
        pass
        if amount_mistakes > (max_mistakes - 1) or time_up == 1:
            #SEND MESSAGE TO REST OF BOMB
            logging.info("Entered the Boom loop")
            logging.info("BOOM!\n\namount_mistakes={}\nactive_module={}\nstatus={}\ntime_up={}".format(amount_mistakes, active_Modules, status, time_up))
            gpio.cleanup()
            exit(0)
    client.loop_stop() #stop the loop