#TODO: Implement that the function will send the message to start blinken from anywhere without repeating and taking to long

#Imports
from pause import until
import logging
import pdc6x1
from time import sleep, time
import paho.mqtt.client as mqtt #import the client1
import json
#-----------------------------------------------
def clock_process(time_total, blinkfrom, DEBUG):
    global defused
    defused = False
    if DEBUG:
        logging.basicConfig(filename='logfile.log', level=logging.DEBUG, format='%(levelname)s: %(asctime)s: %(filename)s: %(funcName)s: \n\t%(message)s')
    if not DEBUG:
        logging.basicConfig(filename='logfile.log', level=logging.WARNING, format='%(levelname)s: %(asctime)s: %(filename)s: %(funcName)s: \n\t%(message)s')

    display = pdc6x1.PDC6x1()
    display.show("  0000", 0, 2)

    time_left = time_total * 100        #Makes the decimel number into an integer that is easyer to work with.
    broker_address="192.168.178.15"     #Sets the adress to whom will be send the message.
    client = mqtt.Client("PTimer")      #Create new instance of mqtt client.
    client.connect(broker_address)      #Connect to broker.
    

    starttime = (time() + 2.5)         #Sets time from where all will start.

#    dictionary1 = ["TimerModule", "R"]                                      #Preset message to tell the main process that this module exists.
#    messageR = json.dumps(dictionary1)                                      # "
    dictionary2 = ["TimerModule", "T"]                                      #Preset message to tell the main process that time's up.
    messageT = json.dumps(dictionary2)                                      # "
    dictionary3 = ["TimerModule", "B", time_total, blinkfrom, starttime]    #Preset message to tell the blinking process to start blinking. (Format: ["SendFrom", "Blinking command", "Total time", "Blink from", startfrom]).
    messageB = json.dumps(dictionary3)                                      # "

    client.publish("main_channel", messageB)    #Tells the blinking process all the peramiters that are needed for it.
#    client.publish("main_channel", messageR)        #Tells the main process that it exists (Send predefined message).

    until(starttime)                                #Waits for all the other time based programs to get ready to start and starts after a predeterment time 2.5 seconds.
    #Start Counting
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    while time_left > 59999 and not defused:
        time1 = time()                                      #Takes current time to determen later how lont to wait for.
        minu1, sec1 = divmod((time_left//100), 60)
        minu2, sec2 = str(minu1), str(sec1)
        if sec1 < 10:
            sec2 = "0" + sec2
        if sec1 == 0:
            sec2 = "00"
        display.show("  {}{}".format(minu2, sec2), 1, 2)
        time_left -= 100                                    #Takes one second from the timer.
        until(time1 + 1.00)                                 #Waits untill one second has passed from the beginning of this while-loop itiration.
        pass

    while 60000 > time_left > 6000 and not defused:                          #Is active when time left > 60 seconds.
        time2 = time()                                      #Takes current time to determen later how lont to wait for.
        minu1, sec1 = divmod((time_left//100), 60)
        minu2, sec2 = str(minu1), str(sec1)
        if sec1 < 10:
            sec2 = "0" + sec2
        if sec1 == 0:
            sec2 = "00"
        display.show("  0{}{}".format(minu2, sec2), 1, 2)
        time_left -= 100                                    #Takes one second from the timer.
        until(time2 + 1.00)                                 #Waits untill one second has passed from the beginning of this while-loop itiration.
        pass
    
    while -1 < time_left < 6001 and not defused:                             #Is activated when time is less than 60.01 seconds and is more them 0.009999999... seconds.
        time3 = time()                                      #Takes current time to determen later how lont to wait for.
        if time_left > 999:
            space = ""
        if time_left < 1000:
            space = "0"
        if time_left < 100:
            space = "00"
        display.show(("  " + space + str(time_left)), 1, 2)#NOGFORMATTEN VAN DE SPACINGK
        time_left -= 1                                      #Takes one hundreth of a second from the timer.
        until(time3 + 0.01)                                 #Waits untill one second has passed from the beginning of this while-loop itiration.
        pass        
        

    while time_left < 1:                            #Is activated when time is less than 0.01 seconds
        display.show("  0000", 1, 2)
        client.publish("main_channel", messageT)    #Tells the main process that Time's up (Send predefined message).
        display.show("      ", 1, 2)
        exit(0)