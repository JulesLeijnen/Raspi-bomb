from draadmodulev1 import *
from Timer import *

import threading


mode_correct = False
DEBUG_correct = False

#---------------------------------------------------------------------------------

def DraadmodeCaller(mode_draad, Custom_colours, testing):
    DRAADmode_selection(mode_draad, Custom_colours, testing)
    return
    
def DraadCheckUICaller():
    Check_UI()
    return


def TimermodeCaller(mode_timer, seconds, blink, testing):
    setupclock(mode_timer, seconds, blink, testing)
    return

#---------------------------------------------------------------------------------

def main():
    global mode_correct, DEBUG_correct, wires
    while not DEBUG_correct:
        testing = input(str("Do you want to use debugging? Answer 1/0"))
        if testing == "1" or testing == "0":
            DEBUG_correct = True
            if testing == "1":
                testing = 1
            else:
                testing = 0
        else:
            print("Input ERROR: Input format incorrect! Choose (1/0)")
            print("Your input was: {}".format(testing))
            pass
    while not mode_correct:
        mode = input(str("What mode do you want? \n Default (D) \n Kids (K) \n Custom (C)")).upper()
        print("You have selected {}".format(mode))
        if mode == "D":
            DRAADSetupgame = threading.Thread(target=DraadmodeCaller, args=("D", 0, testing))
            DRAADSetupgame.start()
            DRAADSetupgame.join()
            input("Wire Setup Compleet, moving onto the Timer after the Enter press. \n Press Enter when you van installed the wires correctly")
            TIMERSetupgame = threading.Thread(target=TimermodeCaller, args=("D", 0, 0, testing))
            TIMERSetupgame.start()
            TIMERSetupgame.join()
            input("Press Enter when your setting up is done.")
            DRAADCheckgame = threading.Thread(target=DraadCheckUICaller)
            DRAADCheckgame.start()
            DRAADCheckgame.join()
            mode_correct = True
            pass
        elif mode == "K":
            DRAADSetupgame = threading.Thread(target=DraadmodeCaller, args=("K", 0, testing))
            DRAADSetupgame.start()
            DRAADSetupgame.join()
            input("Press Enter when your setting up is done.")
            DRAADCheckgame = threading.Thread(target=DraadCheckUICaller)
            DRAADCheckgame.start()
            DRAADCheckgame.join()
            mode_correct = True
            pass
        elif mode == "C":
            mode_correct = True
            pass
        else:
            print("Input ERROR: Input format incorrect! Choose (D/K/C)")
            print("Your input was: {}".format(mode))
            pass
    return

if __name__ == "__main__":
    main()