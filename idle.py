from naoqi import ALProxy
# ### Custom File Handing Imports ###
# from fileTransfer import *

# ### Custom Idle Behaviour Imports ###
# from idle import *

# ### Custom Page Display Imports ###
# from displayGeneration import *

# ### Custom Interaction, Behaviour and Display Imports ###
# from interactiveControls import *

# ### Custom Hard-Coded Prompt Imports ###
# from prompts import *

# ### Main Interaction Imports ###
# from humanInteraction import *


import random, threading, time
import constants
from constants import PEPPER_HOST, PEPPER_PORT

class idling:
    """While not inConversation, then Pepper should be idle"""
    def __init__(self):
        self.idling = None
        self.behavior = ALProxy("ALBehaviorManager", constants.PEPPER_HOST, constants.PEPPER_PORT)
        self.leds = ALProxy("ALLeds", constants.PEPPER_HOST, constants.PEPPER_PORT)
        self.behaviorList = [
            'animations/Stand/Waiting/BackRubs_1', 'animations/Stand/Waiting/FunnyDancer_1', 
            'animations/Stand/Waiting/HideEyes_1', 'animations/Stand/Waiting/HideHands_1', 
            'animations/Stand/Waiting/Innocent_1', 'animations/Stand/Waiting/LookHand_1', 
            'animations/Stand/Waiting/LookHand_2', 'animations/Stand/Waiting/LoveYou_1', 
            'animations/Stand/Waiting/PlayHands_1', 'animations/Stand/Waiting/PlayHands_2', 
            'animations/Stand/Waiting/PlayHands_3', 'animations/Stand/Waiting/Relaxation_1', 
            'animations/Stand/Waiting/Relaxation_2', 'animations/Stand/Waiting/Relaxation_3', 
            'animations/Stand/Waiting/Relaxation_4', 'animations/Stand/Waiting/Rest_1', 
            'animations/Stand/Waiting/ScratchBack_1', 'animations/Stand/Waiting/ScratchBottom_1', 
            'animations/Stand/Waiting/ScratchEye_1',  'animations/Stand/Waiting/ScratchHand_1', 
            'animations/Stand/Waiting/ScratchHead_1', 'animations/Stand/Waiting/ScratchLeg_1', 
            'animations/Stand/Waiting/ScratchTorso_1', 
            'animations/Stand/Waiting/Stretch_1', 'animations/Stand/Waiting/Stretch_2',
            'animations/Stand/Waiting/Think_1', 'animations/Stand/Waiting/Think_2', 
            'animations/Stand/Waiting/Think_3', 'animations/Stand/Waiting/Think_4'
        ]
        self.idle_thread = threading.Thread(target=self.idle_behavior_thread)

    def idle_behavior_thread(self):
        while self.idling:
            behaviorName = random.choice(self.behaviorList)

            # Checks if behavior is installed and not running
            if self.behavior.isBehaviorInstalled(behaviorName):
                # Runs behavior
                self.behavior.runBehavior(behaviorName)
                self.leds.fadeRGB('FaceLeds', 'white', 1)
                time.sleep(15)

            else:
                print("Behavior not found: " + behaviorName)

        return

    def start_idle_behavior(self):
        self.idling = True
        self.idle_thread.start()

    def stop(self):
        self.idling = False
        self.behavior.stopAllBehaviors()
        self.leds.fadeRGB('FaceLeds', 'white', 1)
        self.idle_thread.join(0)