from flask import Flask, render_template, request
from naoqi import ALProxy
import os

app = Flask(__name__)

@app.route('/qrcodes', methods=['POST'])
def show_qrcode():
    course_name = request.form['course_name']

    # Generate the path to the QR code image
    qrcode_path = os.path.join(os.path.dirname(__file__), 'qrcodes', course_name + '.PNG')

    # Get the IP address of the robot
    robot_ip = "10.104.23.217"

    # Create a proxy to ALTabletService
    tablet_service = ALProxy("ALTabletService", robot_ip, 9559)

    # Display the image on the tablet
    tablet_service.showImage(str(qrcode_path))

    return render_template('qrcode.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
