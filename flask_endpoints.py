from flask import Response
from flask import Flask
from flask import render_template
from camera_control import CameraControl
app = Flask(__name__)

camera_control = CameraControl()
camera_control.connect_camera(-1)
camera_control.start()


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


if __name__ == "__main__":
    print("--------------------Running Main--------------------")
    # app.run(debug=True)
    app.run(debug=True, host='0.0.0.0', port=5000)
