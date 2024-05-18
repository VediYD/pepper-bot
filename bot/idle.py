from naoqi     import ALProxy
from random    import choice
from threading import Thread
from time      import sleep, time
from constants import PEPPER_HOST, PEPPER_PORT


class idling:
    """While not inConversation, then Pepper should be idle"""
    def __init__(self):
        self.idling = None
        self.behavior = ALProxy("ALBehaviorManager", PEPPER_HOST, PEPPER_PORT)
        self.leds = ALProxy("ALLeds", PEPPER_HOST, PEPPER_PORT)
        self.behaviorPath = 'animations/Stand/Waiting/'
        self.behaviorList = [
            'BackRubs_1', 
            'FunnyDancer_1', 
            'HideEyes_1', 
            'HideHands_1', 
            'Innocent_1',
            'LookHand_1', 
            'LookHand_2', 
            'LoveYou_1', 
            'PlayHands_1', 
            'PlayHands_2',
            'PlayHands_3', 
            'Relaxation_1', 
            'Relaxation_2', 
            'Relaxation_3', 
            'Relaxation_4',
            'Rest_1', 
            'ScratchBack_1', 
            'ScratchBottom_1', 
            'ScratchEye_1', 
            'ScratchHand_1',
            'ScratchHead_1', 
            'ScratchLeg_1', 
            'ScratchTorso_1', 
            'Stretch_1',
            'Stretch_2',
            'Think_1', 
            'Think_2', 
            'Think_3', 
            'Think_4',
        ]
        self.behaviorList = [self.behaviorPath + beh for beh in self.behaviorList]
        self.idle_thread = Thread(target=self.idle_behavior_thread)
        self.idle_thread.start()

    def idle_behavior_thread(self):
        behavior_interval = 15  # Launch behavior every 15 seconds
        behavior_last_run = 0

        while True:
            current_time = time()

            if self.idling and current_time - behavior_last_run >= behavior_interval:
                behaviorName = choice(self.behaviorList)

                # Checks if behavior is installed and not running
                if self.behavior.isBehaviorInstalled(behaviorName):
                    
                    # Runs behavior
                    self.behavior.runBehavior(behaviorName)
                    self.leds.fadeRGB('FaceLeds', 'white', 1)
                    behavior_last_run = current_time  # Update last behavior run time

                else:
                    print("Behavior not found: " + behaviorName)
            
            sleep(1)  # Check every second

    def start_idle_behavior(self):
        self.idling = True

    def stop(self):
        self.behavior.stopAllBehaviors()
        self.idling = False
        self.leds.fadeRGB('FaceLeds', 'white', 1)
