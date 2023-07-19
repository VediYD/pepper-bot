import os
import qi
from flask import Flask, request, jsonify

app = Flask(__name__)

def connect_to_robot(ip_address, port=9559, username="nao", password="nao"):
    try:
        session = qi.Session()
        session.connect("tcp://{0}:{1}".format(ip_address, port))
        session.service("ALTabletService")
        session.service("ALPhotoCapture")
        return session
    except Exception as e:
        print("Error connecting to the robot: ", e)
        return None

def get_tablet_service(session):
    try:
        tablet_service = session.service("ALTabletService")
        return tablet_service
    except Exception as e:
        print("Error getting the tablet service: ", e)
        return None

def get_absolute_url(session, partial_url):
    if not partial_url.startswith('/'):
        partial_url = '/' + partial_url

    sub_path = os.path.join(session.packageUid(), os.path.normpath(partial_url).lstrip("\\/"))
    return "http://{0}/apps/{1}".format(session.robotIp(), sub_path.replace(os.path.sep, "/"))

def receive_file(local_path, image_path):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("10.104.23.185", username='nao', password='nao')

    sftp = ssh.open_sftp()
    sftp.put(local_path, image_path)

    sftp.close()
    ssh.close()

@app.route("/show_image_from_memory", methods=["POST"])
def show_image_from_memory():
    try:
        course_name = request.form['course_name']

        # Generate the path to the QR code image
        qrcode_path = os.path.join(os.path.dirname(__file__), 'qrcodes', course_name + '.png')

        ip_address = "10.104.23.185"
        session = connect_to_robot(ip_address)
        if not session:
            return jsonify({"status": "error", "message": "Failed to connect to the robot."})

        tablet_service = get_tablet_service(session)
        if not tablet_service:
            return jsonify({"status": "error", "message": "Failed to get ALTabletService."})

        
        # Transfer the image file to Pepper's memory
        image_path = "/home/nao/img/img.png"
        receive_file(qrcode_path, image_path)

        # Display the image on the tablet
        tablet_service.showImage(get_absolute_url(session, image_path))

        return jsonify({"status": "success"})

    except Exception as err:
        return jsonify({"status": "error", "message": str(err)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
