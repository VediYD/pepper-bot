### Custom File Handing Imports ###
from fileTransfer import *

### Custom Idle Behaviour Imports ###
from idle import *

### Custom Page Display Imports ###
from displayGeneration import *

### Custom Interaction, Behaviour and Display Imports ###
from interactiveControls import *

### Custom Hard-Coded Prompt Imports ###
from prompts import *

### Main Interaction Imports ###
from humanInteraction import *

import constants

################################################################################
##### SFTP File Transfer Functions
##########

# def sendFromPepper(pepperSourceFile=PEPPER_RECORDINGS_PATH, serverLandingFile=SERVER_RECORDINGS_PATH):
#     """Get files from Pepper on local (server) machine"""
#     ssh = paramiko.SSHClient()
#     ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#     ssh.connect(PEPPER_HOST, username='nao', password='nao')

#     sftp = ssh.open_sftp()
#     sftp.get(pepperSourceFile, serverLandingFile)

#     sftp.close()
#     ssh.close()
#     print("File transfered")

# def sendToPepper(serverSourceFile=SERVER_RECORDINGS_PATH, pepperLandingFile=PEPPER_RECORDINGS_PATH):
#     """Send files from local (server) machine to Pepper"""
#     ssh = paramiko.SSHClient()
#     ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#     ssh.connect(PEPPER_HOST, username='nao', password='nao')

#     sftp = ssh.open_sftp()
#     sftp.put(serverSourceFile, pepperLandingFile)

#     sftp.close()
#     ssh.close()

def sendFromPepper(pepperSourceFile=constants.PEPPER_RECORDINGS_PATH, serverLandingFile=constants.SERVER_RECORDINGS_PATH):
    """Get files from Pepper on local (server) machine"""
    ssh, sftp = setupSFTP()
    sftp.get(pepperSourceFile, serverLandingFile)
    closeSFTP(ssh, sftp)
    print("Sent from Pepper")

def sendToPepper(serverSourceFile=constants.SERVER_RECORDINGS_PATH, pepperLandingFile=constants.PEPPER_RECORDINGS_PATH):
    """Send files from local (server) machine to Pepper"""
    ssh, sftp = setupSFTP()
    sftp.put(serverSourceFile, pepperLandingFile)
    closeSFTP(ssh, sftp)
    print("Sent to Pepper")

def setupSFTP():
    """open SFTP connection"""
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(PEPPER_HOST, username='nao', password='nao')
    sftp = ssh.open_sftp()
    return ssh, sftp

def closeSFTP(ssh, sftp):
    """close SFTP connection"""
    sftp.close()
    ssh.close()    


def sendFileToPepper(sourceFile, landingFile):
    """take sourceFile and send to landingFile location on Pepper robot"""
    sendToPepper(sourceFile, landingFile)
#    ssh = paramiko.SSHClient()
#    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#    ssh.connect(ip, username='nao', password='nao')

#    sftp = ssh.open_sftp()
#    sftp.put(sourceFile, landingFile)

#    sftp.close()
#    ssh.close()

################################################################################
##### ...
##########
