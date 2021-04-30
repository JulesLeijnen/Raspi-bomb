from random import randrange
from time import sleep
from sys import exit
import logging
#------------------------------------------------------------------------------
#All global variables and where they're used


info_complete_mode = False
info_complete_wires = False
info_complete_timer = False
info_complete_debug = False

DEBUG = False

logging.info("Created global begin var's:\n\tinfo_complete_mode = {}\n\tinfo_complete_wires = {}\n\tinfo_complete_timer = {}\n\tinfo_complete_debug = {}\n\n\tDEBUG = {}".format(info_complete_mode, info_complete_wires, info_complete_timer, info_complete_debug, DEBUG))

    # setup_info_list = [mode, maximum mistakes, timer duration (seconds), timer blink from, Serialnumber, serial last is odd?, serialnumber has vowel, amountwires, wirelist, wires solution]
    # setup_info_list = ["D", 3, 300, 60, "XX1XX1", 0, 0, 4, ["Black", "Red", "White", "Red"], 2]

#------------------------------------------------------------------------------
#DEFINING: Asking all the needed info

def Mode_selecter():

    info_complete_mode = False
    output = []
    
    while not info_complete_mode: #Keeps looping untill a correct mode is entered
        mode = input(str("What mode do you want? \n Default (D) \n Kids (K) \n Custom (C)")).upper() #Asks for input and uppercases it to make it easier to deal with later.
        if mode == "D" or mode == "K" or mode == "C": #Checks if input is correct
            print("You have selected {}".format(mode)) #Print to terminal what is selected
            info_complete_mode = True #A correct input was given, so the loop is broken free from to the next question
            if mode == "C":
                faults = int(input("How many mistakes untill the bomb goes off. pick 1, 2 or 3"))
            if not mode == "C":
                faults = 3
            if not 0 < faults < 4:
                faults = 3
                print("Incorrect input. Setting 3 mistakes as the amount needed to detonate.")
            output.append(mode)
            output.append(faults)
        else:
            print("Incorrect input. Please try again. (Only D, K or C allowed)(Error line:42)") #Lets the user know that they made a mistake and what to input next
    return output

def Wiremodule_setup(used_mode, serial_odd):
    possible_colours = [["Red", "Blue", "White", "Red", "Blue", "White", "Yellow", "Black", "Not_important"],
                        ["Red", "Blue", "Yellow", "Red", "Blue", "Yellow", "White", "Black", "Not_important"],
                        ["Red", "Black", "Yellow", "Red", "Black", "yellow", "White", "Blue", "Not_important"],
                        ["Red", "white", "Yellow", "Red", "white", "yellow", "Black", "Blue", "Not_important"]]

    wires = []
    output = []
    solution = 0
    
    info_complete_wires = False
    custom_wire_compleet = False
    custom_wire_sequence_input_correct = False

    while not info_complete_wires: # Keeps looping intill a correct number of wires is selected.

        if used_mode == "D": #Checks if mode "D" is selected
            amountwires = ((randrange(0,4)+3)) #Generated a random number from 3 to 6
            if 2 < amountwires < 7: #Checks if generated input is correct
                print("Wires amount selected: {}".format(amountwires)) #Shows the user in terminal the selected amount of wires
                output.append(amountwires) #Appends the amount of wires in the module to the second slot in the output array, [1]
                for _ in range(0, amountwires):
                    wires.append(possible_colours[amountwires-3][randrange(0,9)])
                output.append(wires)
                info_complete_wires = True #Breaks free from loop, so that the next input can be given
            else:
                print("Incorrect wire selection. This automated process failed. Now trying again.")
        elif used_mode == "K": #Checks if mode "K" is selected
            amountwires = ((randrange(0,2)+3)) #Generated a random number, 3 or 4
            if 2 < amountwires < 5: #Checks if generated input is correct
                print("Wires amount selected: {}".format(amountwires)) #Shows the user in terminal the selected amount of wires
                output.append(amountwires) #Appends the amount of wires in the module to the second slot in the output array, [1]
                for _ in range(0, amountwires):
                    wires.append(possible_colours[amountwires-3][randrange(0,9)])
                output.append(wires)
                info_complete_wires = True #Breaks free from loop, so that the next input can be given
            else:
                print("Incorrect wire selection. This automated process failed. Now trying again.")

        elif used_mode == "C": #Checks if mode "C" is selected
            amountwires = int(input("How many wires do you want on the module? Select from 3 to 6 (Must be a number)")) #Asks input in termenal for wires amount in module
            if (2 < amountwires < 7): #Checks if generated input is correct
                print("Wires amount selected: {}".format(amountwires)) #Shows the user in terminal the selected amount of wires
                output.append(amountwires) #Appends the amount of wires in the module to the second slot in the output array, [1]
                while not custom_wire_compleet:
                    custom_wire_sequence = input(str("Do you want to make the wire sequence yourself? Y/N")).upper()
                    if custom_wire_sequence == "N":
                        for _ in range(0, amountwires):
                            wires.append(possible_colours[amountwires-3][randrange(0,9)])
                        output.append(wires)
                        custom_wire_compleet = True #Breaks free from loop, so that the next input can be given
                        pass
                    elif custom_wire_sequence == "Y":
                        for x in range(0, amountwires):
                            custom_wire_sequence_input_correct = False
                            while not custom_wire_sequence_input_correct:
                                customwire_temp = input(str("What is colour number {}? Answer with 'Red', 'Blue', 'Yellow', 'White', 'Black' or 'Not_Important'").format(x+1)).capitalize()
                                if customwire_temp in ["Red", "Blue", "Yellow", "White", "Black", "Not_important"]:
                                    wires.append(customwire_temp)
                                    custom_wire_sequence_input_correct = True #Breaks free from loop, so that the next input can be given
                                else:
                                    print("Incorrect input. Please try again. (Only 'Red', 'Blue', 'Yellow', 'White', 'Black', 'Not_important' allowed)")          
                        output.append(wires)
                        custom_wire_compleet = True #Breaks free from loop, so that the next input can be given
                        pass
                    else:
                        print("Incorrect input. Please try again. Y/N (Error line:112)")                        
                info_complete_wires = True #Breaks free from loop, so that the next input can be given
            else:
                print("Incorrect input. Please try again. (Only 3, 4, 5, or 6 allowed)")

        else:
            print(output)
            print("Incorrect input. Please restart program. (Only D, K or C allowed)(Error line:118)") #Lets the user know that they made a mistake and what to input next
            print("Program is now shutting down.")
            sleep(0.3)
            exit(1)

        if amountwires == 3:
            if ((wires.count("Red") == 0) or ((wires.count("Blue") > 1 and wires[2] == "Red"))):
                solution = 2
            else:
                solution = 3  # default waarde

        elif amountwires == 4:
            if (wires.count("Red")) > 1 and serial_odd == 1:
                solution = (4 - 1 - wires[::-1].index('Red') + 1)
            elif (wires[3] == "Yellow" and (wires.count("Red")) == 0) or (wires.count("Blue")) == 1:
                solution = 1
            elif (wires.count("Yellow")) > 1:
                solution = 4
            else:
                solution = 2  # default waarde
        
        elif amountwires == 5:
            if wires[4] == "Black" and serial_odd == 1:
                solution = 4
            elif wires.count("Black") == 0:
                solution = 2
            else:
                solution = 1  # default waarde

        elif amountwires == 6:
            if wires.count("Yellow") == 0 and serial_odd == 1:
                solution = 3
            elif wires.count("Red") == 0:
                solution = 6
            else:
                solution = 4  # default waarde
        else:
            print("Calculation Error. Please restart program. (Error line:155)") #Lets the user know that they made a mistake and what to input next
            print("Program is now shutting down.")
            sleep(0.3)
            exit(1)
        output.append(solution)      
        print(output)

    return output

def timermodule_setup(used_mode):

    info_complete_timer = False
    output = []

    while not info_complete_timer:
        if used_mode == "D":
            output.append(70)
            output.append(60)
            info_complete_timer = True
            print("Mode 'D', timer is 5 minutes and blinks from 60 seconds.")
        elif used_mode == "K":
            output.append(600)
            output.append(60)
            info_complete_timer = True
            print("Mode 'K', timer is 10 minutes and blinks from 60 seconds.")
        elif used_mode == "C":
            timer_length = int(input("How long do you need the timer to be? In seconds."))
            blink_from = int(input("From what time do you want the system to start blinking? In seconds. Max = 60 seconds"))
            if timer_length > 0 and 61 > blink_from > 0:
                output.append(timer_length)
                output.append(blink_from)
                info_complete_timer = True
            else:
                print("Error from incorrect input. Please try again.")
        elif not (used_mode in ["D", "K", "C"]):
            print(output)
            print(used_mode)
            print(type(used_mode))
            print("Incorrect input. Please restart program. (Only D, K or C allowed)(Error line:191)") #Lets the user know that they made a mistake and what to input next
            print("Program is now shutting down.")
            sleep(0.3)
            exit(1)
    return output

def serialmodule_setup(used_mode):

    # XX1XX1

    output = [] # [Serialnumber, is odd?, had Vowel?]
    info_complete_serial = False

    Odd = 0
    Vowel = 0
    Serialnumber = ""

    Vowels = ["A", "E", "O", "U", "I"]
    Non_Vowels = ["B", "C", "D", "F", "G", "H", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "V", "W", "X", "Z"]
    Odds = ["1", "3", "5", "7", "9"]
    Non_Odds = ["2", "4", "6", "8"]
    All_numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9",]

    while not info_complete_serial:
        if used_mode == "D":
            Odd = randrange(0,2)
            Vowel = randrange(0,2)
            pass
        elif used_mode == "K":
            Odd = randrange(0,2)
            Vowel = 0
            pass
        elif used_mode == "C":
            Serialnumber = int(input("What is the serial number? Use format XX1XX1"))
            Odd = int(input("Is the last number of the serial odd? 1 for Yes, 0 for No"))
            Vowel = int(input("Is their a vowel in the serial number? 1 for Yes, 0 for No"))
            pass
        else:
            print(output)
            print("Incorrect input. Please restart program. (Only D, K or C allowed)(Error line:230)") #Lets the user know that they made a mistake and what to input next
            print("Program is now shutting down.")
            sleep(0.3)
            exit(1)
        if Serialnumber == "":
            if Vowel == 0 and Odd == 0:
                Serialnumber = Serialnumber + Non_Vowels[randrange(0,21)] + Non_Vowels[randrange(0,21)] + All_numbers[randrange(0,10)] + Non_Vowels[randrange(0,21)] + Non_Vowels[randrange(0,21)] + Non_Odds[randrange(0,4)]
            elif Vowel == 0 and Odd == 1:
                Serialnumber = Serialnumber + Non_Vowels[randrange(0,21)] + Non_Vowels[randrange(0,21)] + All_numbers[randrange(0,10)] + Non_Vowels[randrange(0,21)] + Non_Vowels[randrange(0,21)] + Odds[randrange(0,5)]
            elif Vowel == 1 and Odd == 0:
                Serialnumber = Serialnumber + Vowels[randrange(0,5)] + Vowels[randrange(0,5)] + All_numbers[randrange(0,10)] + Vowels[randrange(0,5)] + Vowels[randrange(0,5)] + Non_Odds[randrange(0,4)]
            elif Vowel == 1 and Odd == 1:
                Serialnumber = Serialnumber + Vowels[randrange(0,5)] + Vowels[randrange(0,5)] + All_numbers[randrange(0,10)] + Vowels[randrange(0,5)] + Vowels[randrange(0,5)] + Non_Odds[randrange(0,4)]
            info_complete_serial = True
            pass
        else:
            info_complete_serial = True
            pass
        print(Serialnumber)
    output.append(Serialnumber)
    output.append(Odd)
    output.append(Vowel)    

    return output

def setup_main():
    setup_info_list = []

    used_mode = Mode_selecter()
    print(used_mode)
    setup_info_list.append(used_mode[0])
    setup_info_list.append(used_mode[1])
    print(setup_info_list)
    used_timersetup = timermodule_setup(used_mode[0])
    setup_info_list.append(used_timersetup[0])
    setup_info_list.append(used_timersetup[1])
    used_serialsetup = serialmodule_setup(used_mode[0])
    setup_info_list.append(used_serialsetup[0])
    setup_info_list.append(used_serialsetup[1])
    setup_info_list.append(used_serialsetup[2])
    used_wiresetup = Wiremodule_setup(used_mode[0], used_serialsetup[1])
    setup_info_list.append(used_wiresetup[0])
    setup_info_list.append(used_wiresetup[1])
    setup_info_list.append(used_wiresetup[2])
    print(setup_info_list)
    return setup_info_list
