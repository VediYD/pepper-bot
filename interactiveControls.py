from naoqi import ALProxy

import fileTransfer as ft
from fileTransfer import sendToPepper

import displayGeneration as dg
# from displayGeneration import generateDefaultPage, generateDashLoader, generateWelcomePage, generateStudyPage, generateUpperCoursePage, generateAccomodationPage, generateClubPage, generateCampusPage
from displayGeneration import *

import constants, threading, time 
from constants import PEPPER_HOST, PEPPER_PORT, PEPPER_PAGE_LANDING

################################################################################
##### Head Tracking Functions
##########

def track_head(mode="Head"):
    """find face to target and look towards them until ended"""
    tracker = ALProxy("ALTracker", constants.PEPPER_HOST, constants.PEPPER_PORT)
    tracker.unregisterAllTargets()
    tracker.initialize()
    tracker.registerTarget("Face", 0.05)
    tracker.setMode(mode)
    tracker.track("Face")

def stop_track_head():
    """cease track_head()"""
    tracker = ALProxy("ALTracker", constants.PEPPER_HOST, constants.PEPPER_PORT)
    tracker.stopTracker()
    tracker.unregisterAllTargets()



################################################################################
##### Eye Colour Functions
##########

def set_leds(color = 'white', ledSet = 'Face'):
    rgb = None
    if color == "cyan":
        rgb = [0.69, 1, 0.84]

    leds = ALProxy("ALLeds", constants.PEPPER_HOST, constants.PEPPER_PORT)
    if rgb is not None:   
        leds.fadeRGB(ledSet + "Leds", rgb[0], rgb[1], rgb[2], 1)
    else:
        leds.fadeRGB(ledSet + "Leds", color, 1)

# class think_eyes:
class EyesController(object):
    def __init__(self):
        # self.thinking = True
        self.leds = ALProxy("ALLeds", constants.PEPPER_HOST, constants.PEPPER_PORT)
        self.colourList = {
            "thinking" : [0.04, 0.44, 0.38],  # green
            "listening": [0, 0.49, 0.60],     # teal
            "confused" : [0.78, 0.26, 0.60],  # magenta
            "neutral"  : [1, 1, 1]            # white
        }
        self.eyeFade = True
        self.mode = "neutral"
        self.eyeColourThread = None 

    def colourEyes(self):
        while self.eyeFade:
            self.leds.fadeRGB("FaceLeds", 'white', 1)
            time.sleep(1)
            # self.leds.fadeRGB("FaceLeds", 0.6, 1, 0.79, 1)
            self.leds.fadeRGB(
                "FaceLeds", 
                self.colourList[self.mode][0], 
                self.colourList[self.mode][1], 
                self.colourList[self.mode][2], 
                1
            ) 
 
    def startEyes(self, mode):
        """start eye colour thread: one of thinking, listening, confused, neutral"""
        self.mode = mode
        self.eyeColourThread = threading.Thread(target=self.colourEyes)
        self.eyeColourThread.start()

    def setEyes(self, mode):
        """update the eye fade colour: one of thinking, listening, confused, neutral"""
        self.mode=mode
        self.eyeFade = True
        
    def stopEyes(self):
        """hard stop, requires totally new thread to restart"""
        self.eyeFade = False
        self.eyeColourThread.join(0)
        self.leds.fadeRGB("FaceLeds", "white", 1)

################################################################################
##### Posture Manipulation
##########

def return_to_default_pos(sentences = None):
    resetEyesAndTablet()
    # set_leds()   
    stop_track_head()
    defaultPosture()
    # stop_show_on_tablet()

def defaultPosture():
    posture = ALProxy("ALRobotPosture", constants.PEPPER_HOST, constants.PEPPER_PORT)
    posture.goToPosture("Stand", 0.5)

def resetEyesAndTablet():
#     hidePage()
    set_leds()



################################################################################
##### Tablet Page
##########

def showWhichPage(page):
    """Show specific special case pages"""
    if page == "prompt":
        dg.generateDefaultPage()
    elif page == "loading":
        dg.generateDashLoader()
    elif page == "listening":
        dg.generateListeningPage()
    elif page == "Cwel":
        dg.generateWelcomePage()
    elif page == "Cstu":
        dg.generateStudyPage()
    elif page == "Cour":
        dg.generateUpperCoursePage()
    elif page == "Cacc":
        dg.generateAccomodationPage()
    elif page == "Club":
        dg.generateClubPage()
    elif page == "Camp":
        dg.generateCampusPage()
    else:
        dg.generateWelcomePage()
    showPage()

def show_on_tablet(path):
    # if path == 'loading_page':
    #     path = './pages/dashLoader.html'
    ft.sendToPepper(path, constants.PEPPER_PAGE_LANDING)
    # receive_file(path, '/home/nao/.local/share/PackageManager/apps/robot-page/html/page.html')
    tabletService = ALProxy("ALTabletService", constants.PEPPER_HOST, constants.PEPPER_PORT)
    tabletService.loadUrl('http://198.18.0.1/page.html')
    tabletService.showWebview()

def stop_show_on_tablet():
    """hide the HTML viewer on Pepper"""
    tabletService = ALProxy("ALTabletService", constants.PEPPER_HOST, constants.PEPPER_PORT)
    tabletService.hideWebview()

# Alt versions (can be removed if refactored)

def showPage():
    """use ALTabletService to show html on Pepper"""
    tabletService = ALProxy("ALTabletService", constants.PEPPER_HOST, constants.PEPPER_PORT)
    tabletService.loadUrl('http://198.18.0.1/page.html')
    tabletService.showWebview()
    
def hidePage():
    """use ALTabletService to hide html from Pepper"""
    tabletService = ALProxy("ALTabletService", constants.PEPPER_HOST, constants.PEPPER_PORT)
    tabletService.hideWebview()




################################################################################
##### Whole Body Language
##########

def startListeningBL():
    dg.generateDashLoader()
    showPage()


