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

import constants, shutil, fileinput
import pandas as pd
from constants import FILE_NAME_TEMP, TEXT_BY_ID_PATH, PEPPER_QR_LANDING, PEPPER_IMG_LANDING, PEPPER_PAGE_LANDING, PEPPER_HTML_PATH
from interactiveControls import showPage
from fileTransfer import sendFileToPepper
from bs4 import BeautifulSoup
import fileTransfer as ft
import re

################################################################################
##### File Setup
##########


### Modules
#import os
#import sys
#import fileinput
#import shutil
#import pandas as pd
#import paramiko
#from naoqi import ALProxy

### File Mapping
#PEPPER_HOST = "10.104.23.185"
#PEPPER_PORT = "9559"
#constants.FILE_NAME_TEMP = "display.html"
#PEPPER_HTML_PATH = "/home/nao/.local/share/PackageManager/apps/robot-page/html/"  # page.html"
#constants.PEPPER_PAGE_LANDING = PEPPER_HTML_PATH + "page.html"
#constants.PEPPER_QR_LANDING = PEPPER_HTML_PATH + "webfiles/qr.png"  # switched slash direction
#constants.PEPPER_IMG_LANDING = PEPPER_HTML_PATH + "webfiles/img.png"  # switched slash direction
#constants.TEXT_BY_ID_PATH = "pages/textbyID.csv"

PATH_PREFIX = ""
IMG_FILES_FOLDER = "ImgFiles/"
QR_CODES_FOLDER = "QRCodes/"


###
def pepperLog(log):
    """Dummy function for error logging"""
    print(log)


### Template list:
# .__________
# | course templates: "basicQRPage.html", "topBannerQRPage.html"
# | other templates: "bottomBannerQRPage.html", "bottomBannerWithBodyQRPage.html", "onlyTextAndImgPage.html"
# | no dependencies: "dashLoader.html", "defaultPage.html"
# |__________


################################################################################
##### Generic Functions
##########


##########
##### Step 1: Generate new html file from template
##########


def duplicateTemplate(type):
    """duplicate file from template (will overwrite)"""
    template = "pageTemplates/" + type  # "basicQRPage.html"
    # fileName = "display.html"
    try:
        shutil.copyfile(template, constants.FILE_NAME_TEMP)
        pepperLog("copyfile successful")
    except:
        pepperLog("copyfile exception occurred")


##########
##### Step 2: Get text elements from csv file
##########

def seekCourseName(ID):
    """find CourseName by ID in library"""
    try:
        data = pd.read_csv(constants.TEXT_BY_ID_PATH)
        text = data.loc[data["ID"] == ID]
        courseName = text.iloc[0]["CourseName"]
    except: 
        courseName = "not found"
    return courseName


def seekLocationText(ID):
    """find LocationText by ID in library"""
    try:
        data = pd.read_csv(constants.TEXT_BY_ID_PATH)
        text = data.loc[data["ID"] == ID]
        locationText = text.iloc[0]["locationText"]
    except: 
        locationText = "not found"
    return locationText


def seekHeadText(ID):
    """find HeadText by ID in library"""
    return ID  # headText


def seekBodyText(ID):
    """find bodyText by ID in library"""
    return ID  # bodyText


def seekCourseAndLocationText(ID):
    """find both CourseName and LocationText by ID in library"""
    try:
        data = pd.read_csv(constants.TEXT_BY_ID_PATH)
        text = data.loc[data["ID"] == ID]
        courseName = text.iloc[0]["CourseName"]
        locationText = text.iloc[0]["locationText"]
    except:
        courseName = "not found"
        locationText = "not found"
    return courseName, locationText

def seekCourseNameList(courseIDList):
    """find CourseName for all items in a list, by ID in library, and return as formatted HTML list"""
    courseListString = ""
    for courseID in courseIDList:
        courseName = seekCourseName(courseID)
        courseListString += " <li> " + courseName + " </li> "
    return courseListString



##########
##### Step 3: Update text elements in new html file
##########


# def textSub(tempText, subText):
#     """find text in file and replace with other text"""
#     textToCut = tempText  # "replaceCourseText"
#     textToPaste = subText  # "the replacement text"
#     # fileName = "display.html"

#     tempFile = open(constants.FILE_NAME_TEMP, "r")
#     tempWrite = open(constants.FILE_NAME_TEMP, "w")
#     matchSuccess = False
#     for line in fileinput.input(constants.FILE_NAME_TEMP):
#         if textToCut in line:
#             matchSuccess = True
#             tempWrite.write(line.replace(textToCut, textToPaste))
#     tempFile.close()

#     if matchSuccess:
#         pepperLog("text match found")
#     else:
#         pepperLog("text match exception occurred")

def textSub(tempText, subText):
    soup = BeautifulSoup(open(constants.FILE_NAME_TEMP), "html.parser")
    target = soup.find(text=re.compile(tempText))

    matchSuccess = False
    if target:
        matchSuccess = True
        target.replace_with(target.replace(tempText, subText))

        # Write the changes back to the HTML file
        with open(constants.FILE_NAME_TEMP, "w") as file:
            file.write(str(soup))


    if matchSuccess:
        pepperLog("text match found")
    else:
        pepperLog("text match exception occurred")


###
# relevant for other templates: "bottomBannerQRPage.html", "bottomBannerWithBodyQRPage.html", "onlyTextAndImgPage.html"
def subHeadText(subText):
    """text sub for specific types: head text"""
    tempText = "replaceHeadText"
    textSub(tempText, subText)


### text sub for specific types: body text
# relevant for other templates: "bottomBannerWithBodyQRPage.html", "onlyTextAndImgPage.html"
def subBodyText(subText):
    """text sub for specific types: body text"""
    tempText = "replaceBodyText"
    textSub(tempText, subText)


### text sub for specific types: Course text
# relevant for course templates: "basicQRPage.html", "topBannerQRPage.html"
def subCourseText(subText):
    """text sub for specific types: course text"""
    # id_df = pd.read_csv(constants.TEXT_BY_ID_PATH)
    # tempText = id_df.loc[id_df["ID"] == subText]["CourseName"]
    tempText = "replaceCourseText"
    textSub(tempText, subText)


### text sub for specific types: Location text
# relevant for course templates: "basicQRPage.html", "topBannerQRPage.html"
def subLocationText(subText):
    """text sub for specific types: location text"""
    # tempText = id_df.loc[id_df["ID"] == subText]["locationText"]
    tempText = "replaceLocationText"
    textSub(tempText, subText)


### text sub for specific types: both Course and Location text
# relevant for course templates: "basicQRPage.html", "topBannerQRPage.html"
def subCourseAndLocationText(subtexts):
    """text sub for specific types: both Course and Location text"""
    subCourseText, subLocationText = subtexts[:]
    #     subLocationText = subtexts[1]
    tempCourseText = "replaceCourseText"
    tempLocationText = "replaceLocationText"
    textSub(tempCourseText, subCourseText)
    textSub(tempLocationText, subLocationText)

### text sub for specific types: list text
# relevant for other templates: "basicListViewPage.html"
def subListText(subText):
    """text sub for specific types: list text"""
    tempText = "replaceListText"
    textSub(tempText, subText)


##########
##### Step 4: Get Visual Elements from local folders
##########


def seekQR(ID):
    """find QR code in library and move to location"""
    ### find QR code in library
    pathToQR = PATH_PREFIX + QR_CODES_FOLDER + ID + ".png" #"QRCodes/"
    ### move QR code to file location as "webfiles\qr.png"
    sendFileToPepper(pathToQR, constants.PEPPER_QR_LANDING)


def seekImg(ID):
    """find QR code in library and move to location"""
    ### find img in library
    pathToImg = PATH_PREFIX + IMG_FILES_FOLDER + ID + ".png" #"imgFiles/"
    ### move img to file location as "webfiles\img.png"
    sendFileToPepper(pathToImg, constants.PEPPER_IMG_LANDING)


##########
##### Step 5: Send updated HTML to Pepper
##########

#def sendFileToPepper(sourceFile, landingFile):
#    """take sourceFile and send to landingFile location on Pepper robot"""
#    ssh = paramiko.SSHClient()
#    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#    ssh.connect(ip, username='nao', password='nao')

#    sftp = ssh.open_sftp()
#    sftp.put(sourceFile, landingFile)

#    sftp.close()
#    ssh.close()

def sendPage():
    """take display.html and push to live"""
    # to send a file to Pepper, call receive_file(local_path="recordings/recording.wav", remote_path="/home/nao/microphones/recording.wav")
    ft.sendFileToPepper(constants.FILE_NAME_TEMP, constants.PEPPER_PAGE_LANDING)
    # showPage()

#def showPage():
#    """use ALTabletService to show html on Pepper"""
#    tabletService = ALProxy("ALTabletService", PEPPER_HOST, PEPPER_PORT)
#    tabletService.loadUrl('http://198.18.0.1/page.html')
#    tabletService.showWebview()


################################################################################
##### Task-Specific Functions
##########

### Group Function Calls


def seekAndSend(ID):
    ### combine all three post tasks for neatness
    seekQR(ID)
    seekImg(ID)
    sendPage()


### Template-Specific Page Generators


def generateBasicQRPage(ID):
    """basicQRPage.html requires img, qr, courseText, locationText. Shows courseText as large text across half-width (left) top-of-page banner, wrapped for up to 3 lines"""
    ### basicQRPage.html requires img, qr, courseText, locationText
    duplicateTemplate("basicQRPage.html")
    subCourseAndLocationText(seekCourseAndLocationText(ID))
    # subCourseText(seekCourseName(ID))
    # subLocationText(seekLocationText(ID))
    seekAndSend(ID)


def generateTopBannerQRPage(ID):
    """topBannerQRPage.html requires img, qr, courseText, locationText. Shows courseText as large text across full-width top-of-page banner"""
    ### topBannerQRPage.html requires img, qr, courseText, locationText
    duplicateTemplate("topBannerQRPage.html")
    subCourseText(seekCourseName(ID))
    subLocationText(seekLocationText(ID))
    seekAndSend(ID)


def generateBottomBannerQRPage(headText, ID):
    """bottomBannerQRPage.html requires img, qr, headText. Shows headtext as large text across half-width (right) bottom-of-page banner"""
    ### bottomBannerQRPage.html requires img, qr, headText
    duplicateTemplate("bottomBannerQRPage.html")
    subHeadText(headText)
    seekAndSend(ID)


def generateBottomBannerWithBodyQRPage(headText, bodyText, ID):
    """bottomBannerWithBodyQRPage.html requires img, qr, headText, bodyText. Shows headtext as large text across half-width (right) bottom-of-page banner, with bodyText beneath"""
    ### bottomBannerWithBodyQRPage.html requires img, qr, headText, bodyText
    duplicateTemplate("bottomBannerWithBodyQRPage.html")
    subHeadText(headText)
    subBodyText(bodyText)
    seekAndSend(ID)


def generateOnlyTextAndImgPage(headText, bodyText, ID):
    """onlyTextAndImgPage.html requires img, headText, bodyText. Shows fullscreen img with partially transparent textbox on bottom-left"""
    ### onlyTextAndImgPage.html requires img, headText, bodyText
    duplicateTemplate("onlyTextAndImgPage.html")
    subHeadText(headText)
    subBodyText(bodyText)
    seekImg(ID)
    sendPage()

def generateBasicListViewPage(IDList):
    """basicListViewPage.html requires img, IDList. Pulls img from 1st ID. Vertical space lists maximum 5 courses"""
    ### basicListViewPage.html requires img, IDList
    duplicateTemplate("basicListViewPage.html")
    courseListText = seekCourseNameList(IDList)
    subListText(courseListText)
    seekImg(IDList[0])
    sendPage()


################################################################################
##### Page-Specific Functions
##########

##########
##### DashLoader
##########


def generateDashLoader():
    """A dynamic loading screen with a cute looping animation"""
    ### dashLoader.html has no requirements
    duplicateTemplate("dashLoader.html")
    sendPage()


##########
##### PromptPage
##########


def generateDefaultPage():
    """A static loading screen with 5 prompts"""
    ### defaultPage.html has no requirements
    duplicateTemplate("defaultPage.html")
    sendPage()


##########
##### ListeningPage
##########


def generateListeningPage():
    """A dynamic listening screen with a cute pulsing animation"""
    ### listeningPage.html has no requirements
    duplicateTemplate("listeningPage.html")
    sendPage()

##########
##### WelcomePage
##########


def generateWelcomePage():
    """using onlyTextAndImgPage.html and ID=Cwel"""
    cwelHeadText = "Welcome to Open Day"
    cwelBodyText = "Experience your tomorrow"
    cwelID = "Cwel"
    generateOnlyTextAndImgPage(cwelHeadText, cwelBodyText, cwelID)


##########
##### UpperCoursePage
##########


def generateUpperCourseQRPage():
    """using generateBottomBannerWithBodyQRPage.html and ID=Cour"""
    courHeadText = "Ready to find your dream course?"
    courBodyText = "At Deakin you won't just learn about the future, you'll prepare for it with real-world learning fuelled by progressive thinking. Explore our practical, industry-shaped courses and get ready to launch a career with impact."
    courID = "Cour"
    generateBottomBannerWithBodyQRPage(courHeadText, courBodyText, courID)


def generateUpperCoursePage():
    """using onlyTextAndImgPage.html and ID=Cour"""
    courHeadText = "Ready to find your dream course?"
    courBodyText = "At Deakin you won't just learn about the future, you'll prepare for it with real-world learning fuelled by progressive thinking. Explore our practical, industry-shaped courses and get ready to launch a career with impact."
    courID = "Cour"
    generateOnlyTextAndImgPage(courHeadText, courBodyText, courID)


##########
##### StudyPage
##########


def generateStudyPage():
    """using generateBottomBannerWithBodyQRPage.html and ID=Cstu"""
    cstuHeadText = "Study"
    cstuBodyText = "Join a world-class university and be ready to take on tomorrow with confidence. At Deakin you won't just learn about the future, you'll prepare for it with real-world learning fuelled by progressive thinking."
    cstuID = "Cstu"
    generateBottomBannerWithBodyQRPage(cstuHeadText, cstuBodyText, cstuID)


##########
##### AccomodationPage
##########


def generateAccomodationPage():
    """using generateBottomBannerWithBodyQRPage.html and ID=Cacc"""
    caccHeadText = "Accommodation"
    caccBodyText = "From our modern on-campus accommodation to a wide range of local, off-campus lodgings; long or short-term, there's a room or house to welcome you."
    caccID = "Cacc"
    generateBottomBannerWithBodyQRPage(caccHeadText, caccBodyText, caccID)


##########
##### ClubsPage
##########


def generateClubPage():
    """using generateBottomBannerWithBodyQRPage.html and ID=Club"""
    clubHeadText = "Clubs and societies"
    clubBodyText = "Uni isn't just about books and study - you're also here to meet new people, try new things, share knowledge and discover your hidden talents. Make the most of your time at Deakin by joining one of our clubs and societies."
    clubID = "Club"
    generateBottomBannerWithBodyQRPage(clubHeadText, clubBodyText, clubID)


##########
##### CampusPage
##########


def generateCampusPage():
    """using generateBottomBannerWithBodyQRPage.html and ID=Camp"""
    campHeadText = "Campuses"
    campBodyText = "Prepare for the jobs of tomorrow in world-class facilities that facilitate progressive, real-world learning. You'll have access to the tools and technology to turn inspiration into creation."
    campID = "Camp"
    generateBottomBannerWithBodyQRPage(campHeadText, campBodyText, campID)

