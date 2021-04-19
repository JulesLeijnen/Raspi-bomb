#All imports:
from random import randrange
import sys
import logging

#------------------------------------------------------------------------------

if __name__ == "__main__":
    info_complete_debug = False
    debug_asking = input(str("Debug on? Y/N")).upper()
    while not info_complete_debug:
        if debug_asking == "Y":
            DEBUG = True
            info_complete_debug = True
        elif debug_asking == "N":
            DEBUG = False
            info_complete_debug = True
        else:
            pass
    if DEBUG:
        logging.basicConfig(filename='logfile.log', level=logging.DEBUG, format='%(levelname)s: %(asctime)s: %(filename)s: %(funcName)s: \n\t%(message)s')
    if not DEBUG:
        logging.basicConfig(filename='logfile.log', level=logging.WARNING, format='%(levelname)s: %(asctime)s: %(filename)s: %(funcName)s: \n\t%(message)s')
    logging.critical("\n\n\n\n")

#------------------------------------------------------------------------------

from time import sleep
from Module_setup import *
from main_process import *
from wire_process import *
from timer_process import *
import multiprocessing

#------------------------------------------------------------------------------
#   Setting up the logging settings
#       DEBUG: detailed information, typically of intrest only when diagnosing problems.
#       INFO: Confirmation that things are working as expected.
#       WARNING: An indication that something unexpected happend, or indicative of some problem in the near future (e.g. 'disk space low')
#       ERROR: Due to a more serious problem, the software has not been able to preform some function
#       CRITICAL: A serious error, indicating that the program itself may be unstable to continue running
#------------------------------------------------------------------------------

def main(DEBUG):
    module_info = setup_main() # This function will ask en sort all info needed to set up the bomb. See Module_setup.py for more info
    #Setup threads
    logging.info("In main: \n\t{}".format(module_info))
    input("Press enter to start the processes")
    main_multiprocess = multiprocessing.Process(target=main_process, args=(module_info[1],))
    wires_multiprocess = multiprocessing.Process(target=Check_UI, args=(module_info[8], module_info[9], DEBUG))
    timer_multiprocess = multiprocessing.Process(target=clock_process, args=(module_info[2], module_info[3], DEBUG))
    main_multiprocess.start()
    sleep(1)
    wires_multiprocess.start()
    sleep(1)
    timer_multiprocess.start()
    logging.info("Started the 'main', 'wires' and 'timer' process")
    
    main_multiprocess.join()
    wires_multiprocess.join()
    timer_multiprocess.join()
    return

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

if __name__ == '__main__':
    main(DEBUG)
else:
    exit(1)