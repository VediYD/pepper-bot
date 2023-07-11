from flask import Flask, render_template, request, send_from_directory
import os
from naoqi import ALProxy

app = Flask(__name__)
image_folder = 'images'
pepper_ip = '10.104.23.217'
pepper_port = 9559

# Initialize the ALTabletService proxy
tablet_service = ALProxy("ALTabletService", pepper_ip, pepper_port)


@app.route('/')
def home():
    # Get a list of all image filenames in the image folder
    images = [filename for filename in os.listdir(image_folder) if filename.endswith(('.jpg', '.png', '.jpeg'))]
    return render_template('index.html', images=images)


@app.route('/images/<filename>')
def serve_image(filename):
    return send_from_directory(image_folder, filename)


@app.route('/display', methods=['POST'])
def display_image():
    # Get the selected image from the request
    selected_image = request.form['selected_image']

    # Display the image on Pepper's tablet screen
    image_path = os.path.join(image_folder, selected_image)
    tablet_service.showImage(image_path)

    return "Image displayed on Pepper's tablet screen"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
