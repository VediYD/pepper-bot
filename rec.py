from flask import Flask, render_template, request
from naoqi import ALProxy
import os
import paramiko

app = Flask(__name__)


def receive_file(local_path, remote_path):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("10.104.23.185", username='nao', password='nao')

    sftp = ssh.open_sftp()
    sftp.put(local_path, remote_path)

    sftp.close()
    ssh.close()
    
    
@app.route('/qrcodes', methods=['POST'])
def show_qrcode():
    course_name = request.form['course_name']

    # Generate the path to the QR code image
    qrcode_path = os.path.join(os.path.dirname(__file__), 'qrcodes', course_name + '.png')

    # Transfer the image file to Pepper's memory
    remote_path = "/home/nao/img/img.png"
    receive_file(qrcode_path, remote_path)

    # Get the IP address of the robot
    robot_ip = "10.104.23.185"

    # Create a proxy to ALTabletService
    tablet_service = ALProxy("ALTabletService", robot_ip, 9559)

    # Display the image on the tablet
    tablet_service.wakeUp()
    tablet_service.showImage(str(remote_path))

    return render_template('qrcode.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
