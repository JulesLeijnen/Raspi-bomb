#All imports:
from random import randrange
from sys import exit
from time import sleep
from Module_setup import *
from main_process import *
from wire_process import *
import threading

#------------------------------------------------------------------------------
#All global variables and where they're used


#------------------------------------------------------------------------------
#DEFINING: Setting up all the modules

#------------------------------------------------------------------------------
#DEFINING: Running the bomb with multiprocessing or threading

#------------------------------------------------------------------------------
#DEFINING: Main
def main():
    module_info = setup_main() # This function will ask en sort all info needed to set up the bomb. See Module_setup.py for more info
    #Setup threads
    print("In main: {}".format(module_info))
    x = input("Write down")
    main_thread = threading.Thread(target=main_process)
    wires_thread = threading.Thread(target=Check_UI, args=(module_info[8], module_info[9]))
    main_thread.start()
    sleep(1)
    wires_thread.start()
    main_thread.join()
    wires_thread.join()
    return
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
if __name__ == '__main__':
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
    main()
else:
    exit(1)