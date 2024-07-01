from paramiko  import SSHClient, AutoAddPolicy
from constants import PEPPER_HOST, PEPPER_PORT
from constants import PEPPER_RECORDINGS_PATH, SERVER_RECORDINGS_PATH

################################################################################
##### SFTP File Transfer Functions
##########

def sendFromPepper(pepperSourceFile=PEPPER_RECORDINGS_PATH, serverLandingFile=SERVER_RECORDINGS_PATH):
    """Get files from Pepper on local (server) machine"""
    ssh, sftp = setupSFTP()
    sftp.get(pepperSourceFile, serverLandingFile)
    closeSFTP(ssh, sftp)
    print("Sent from Pepper")

def sendToPepper(serverSourceFile=SERVER_RECORDINGS_PATH, pepperLandingFile=PEPPER_RECORDINGS_PATH):
    """Send files from local (server) machine to Pepper"""
    ssh, sftp = setupSFTP()
    sftp.put(serverSourceFile, pepperLandingFile)
    closeSFTP(ssh, sftp)
    print("Sent to Pepper")

def setupSFTP():
    """open SFTP connection"""
    ssh = SSHClient()
    ssh.set_missing_host_key_policy(AutoAddPolicy())
    ## these shouldnt be hardcoded and added to the repo in any capacity
    ## this is very risky!!!
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

################################################################################
##### ...
##########
