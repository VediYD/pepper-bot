import naoqi
from naoqi import qi
import time


def getBehaviors(behavior_mng_service):
    """
    Know which behaviors are on the robot.
    """
    names = behavior_mng_service.getInstalledBehaviors()
    print "Behaviors on the robot:"
    print names
    
    names = behavior_mng_service.getRunningBehaviors()
    print "Running behaviors:"
    print names
    
    names = behavior_mng_service.getDefaultBehaviors()
    print "Default behaviors:"
    print names
    

ip = '10.104.23.185'
port = '9559'

session = qi.Session()
session.connect("tcp://" + ip + ":" + port)
service = session.service("ALBehaviorManager")
# getBehaviors(service)


def launchAndStopBehavior(behavior_mng_service, behavior_name):
    """
    Launch and stop a behavior, if possible.
    """
    # Check that the behavior exists.
    if (behavior_mng_service.isBehaviorInstalled(behavior_name)):
        # Check that it is not already running.
        if (not behavior_mng_service.isBehaviorRunning(behavior_name)):
            # Launch behavior. This is a blocking call, use _async=True if you do not
            # want to wait for the behavior to finish.
            behavior_mng_service.runBehavior(behavior_name, _async=True)
            time.sleep(0.5)
        else:
            print "Behavior is already running."

    else:
        print "Behavior not found."
    return

    names = behavior_mng_service.getRunningBehaviors()
    print "Running behaviors:"
    print names

    # Stop the behavior.
    if (behavior_mng_service.isBehaviorRunning(behavior_name)):
        behavior_mng_service.stopBehavior(behavior_name)
        time.sleep(1.0)
    else:
        print "Behavior is already stopped."

    names = behavior_mng_service.getRunningBehaviors()
    print "Running behaviors:"
    print names
