import pathlib
from flask import Response
from flask import Flask
from flask import render_template
from camera_control import CameraControl

IMAGE_PATH = "image_output"

app = Flask(__name__)


def get_last_image_index():
    jpeg_folder_path = pathlib.Path(IMAGE_PATH).resolve()
    jpeg_file_paths = sorted(jpeg_folder_path.rglob('*.jpg'), key=lambda path: int(path.stem.rsplit("_", 1)[1]))
    if jpeg_file_paths:
        return int(jpeg_file_paths[-1].stem.rsplit("_", 1)[1])
    return 0

start_index = get_last_image_index() + 1
camera_control = CameraControl(start_index)
camera_control.connect_camera('/dev/video0')
camera_control.start()
print(camera_control.get_camera_metadata())

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/video_feed")
def video_feed():
    return Response(camera_control.get_live_frame(), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/increase_focus", methods=['POST'])
def increase_focus():
    camera_control.increase_focus()
    return {}, 200


@app.route("/decrease_focus", methods=['POST'])
def decrease_focus():
    camera_control.decrease_focus()
    return {}, 200


@app.route("/set_auto_focus", methods=['POST'])
def set_auto_focus():
    camera_control.set_auto_focus()
    return {}, 200

@app.route("/zero_focus", methods=['POST'])
def zero_focus():
    camera_control.zero_focus()
    return {}, 200


if __name__ == "__main__":
    print("--------------------Running Main--------------------")
    # app.run(debug=True)
    app.run(debug=True, host='0.0.0.0', port=5000)
