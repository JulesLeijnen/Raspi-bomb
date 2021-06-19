#TODO:
# Make a better wire_process.py
# Implement a stop from message (MQTT) in wire_process.py
# Implement Logging in all processes (Main_process and MainV2 allready done.)
# Clean up Imports


#All imports:
import logging

from pause import until
import RPi.GPIO as gpio
import paho.mqtt.client as mqtt #import the client1
from time import sleep, time
import json
import logging

import RPi.GPIO as gpio

from random import randrange
from sys import exit
import logging

from time import sleep          #Imports sleep from the time module
from Module_setup import *      #Imports all info from the needed module
from main_process import *      #Imports all info from the needed module
from wire_process import *      #Imports all info from the needed module
from timer_process import *     #Imports all info from the needed module
from blinking_process import *
import multiprocessing          #Imports multiprocessing to make the modules run in paralel

import spidev
import segment_mapper

from pause import until
import logging
import pdc6x1
from time import sleep, time
import paho.mqtt.client as mqtt #import the client1
import json

from random import randrange, choice
import RPi.GPIO as gpio
import paho.mqtt.client as mqtt #import the client1
import json
import logging

#------------------------------------------------------------------------------

if __name__ == "__main__":
    info_complete_debug = False                                                             #Creates temperary variable to keep a loop running
    while not info_complete_debug:                                                          #Keeps a loop running untill a good answer is given
        debug_asking = input(str("Debug on? Y/N")).upper()                                  #Asking for the mode (uses .upper() to make capitalization not an issue)
        if debug_asking == "Y":                                                             #Checks of the answer is "Y"
            DEBUG = True                                                                    #Sets DEBUG variable used in all processes to change the behavior/output/logging
            info_complete_debug = True                                                      #Changes variable to break free of a loop
        elif debug_asking == "N":                                                           #Checks of the answer is "N"
            DEBUG = False                                                                   #Sets DEBUG variable used in all processes to change the behavior/output/logging
            info_complete_debug = True                                                      #Changes variable to break free of a loop
        else:                                                                               #Executes if input was incorrect
            print("INIT_MAIN: Incorrect input, yours was {}. Only use y/n/Y/Y".format(debug_asking))   #Tells user that there is an issue with their input, and shows their input
    if DEBUG:                                                                               #Checks if DEBUG is True
        logging.basicConfig(filename='logfile.log', level=logging.DEBUG, format='%(levelname)s: %(asctime)s: %(filename)s: %(funcName)s: \n\t%(message)s') #Sets logging details
    if not DEBUG:                                                                           #Checks if DEBUG is False
        logging.basicConfig(filename='logfile.log', level=logging.WARNING, format='%(levelname)s: %(asctime)s: %(filename)s: %(funcName)s: \n\t%(message)s') #Sets logging details
    logging.critical("\n\n\n\n\n\n")                                                        #Creates space so that you can tell sesions apart.

#------------------------------------------------------------------------------



#------------------------------------------------------------------------------
#   Setting up the logging settings
#       DEBUG: detailed information, typically of intrest only when diagnosing problems.
#       INFO: Confirmation that things are working as expected.
#       WARNING: An indication that something unexpected happend, or indicative of some problem in the near future (e.g. 'disk space low')
#       ERROR: Due to a more serious problem, the software has not been able to preform some function
#       CRITICAL: A serious error, indicating that the program itself may be unstable to continue running
#------------------------------------------------------------------------------

def main(DEBUG):
    module_info = setup_main()                                                                                          # This function will ask en sort all info needed to set up the bomb. See Module_setup.py for more info
    print("INIT_MAIN: In main: \n\t{}".format(module_info))                                                                 #Logs all the peramiters used by the different modules
    input("Press enter to start the processes")                                                                         #Waits for use input before continuing
    main_multiprocess = multiprocessing.Process(target=main_process, args=(module_info[1],))                            #Creates the main counting process and stores it in a variable
    wires_multiprocess = multiprocessing.Process(target=Check_UI, args=(module_info[8], module_info[9], DEBUG))         #Creates the wire module process and stores it in a variable
    timer_multiprocess = multiprocessing.Process(target=clock_process, args=(module_info[2], module_info[3], DEBUG))    #Creates the timer module process and stores it in a variable
    blink_multiprocess = multiprocessing.Process(target=Blinker_Process, args=(DEBUG,))
    main_multiprocess.start()
    sleep(4)
    blink_multiprocess.start()
    sleep(4)                                                                                                            #Is not needed, it is a bit of superstition
    wires_multiprocess.start()                                                                                          #Starts wire process
    sleep(4)                                                                                                            #Is not needed, it is a bit of superstition
    timer_multiprocess.start()                                                                                          #Starts Timer process
    print("INIT_MAIN: Started the 'main', 'wires' and 'timer' process")                                                     #Logs that all processes have been started
    
    main_multiprocess.join()                                                                                            #Not desided what to do with them.. Might not need them
    wires_multiprocess.join()                                                                                           #Not desided what to do with them.. Might not need them
    timer_multiprocess.join()                                                                                           #Not desided what to do with them.. Might not need them
    blink_multiprocess.join()
    gpio.cleanup()
    exit(0)
    return

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

if __name__ == '__main__':                                                                                              #Makes sure the bomb is booted from this file, and not as a module of another file
    main(DEBUG)                                                                                                         #Executes the main function and tells it the DEBUG state
else:                                                                                                                   #If executed as a variable, I don't want the bomb to run
    exit(1)                                                                                                             #Exits the program and 