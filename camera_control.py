import cv2
import time
import threading

# 30 frames per second * 60 seconds in a minute * 6.3333 minutes = 11400 frames
# 68400 seconds between 3 and 22 / 11400 frames = 1 frame capture every 6 seconds

IMAGE_PATH = "image_output"
JPG_EXT = ".jpg"


def get_hour():
    return int(time.strftime("%H"))

def get_day():
    return int(time.strftime('%j'))


class CameraControl(threading.Thread):
    WIDTH = 1280
    HEIGHT = 720
    VIDEO_FPS = 20
    focus_increment = 5
    # seconds
    capture_rate = 6
    save_index = 0

    start_hour = 3
    end_hour = 22

    lock = threading.Lock()
    capture = None
    image = None
    running = False
    frame_saved = False

    def __init__(self, start_index=0):
        threading.Thread.__init__(self, daemon=True)
        self.save_index = start_index
        print(cv2.__version__)
        print(self.save_index)

    def __del__(self):
        self.running = False
        if self.capture:
            self.capture.release()

    def connect_camera(self, camera_bus):
        self.capture = cv2.VideoCapture(camera_bus, cv2.CAP_V4L2)
#        error = self.capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        error = self.capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('H', '2', '6', '4'))
        print(f"ERROR CODE: {error}, FOURCC")
        error = self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.WIDTH)
        print(f"ERROR CODE: {error}, WIDTH")
        error = self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.HEIGHT)
        print(f"ERROR CODE: {error}, HEIGHT")
        error = self.capture.set(cv2.CAP_PROP_FPS, self.VIDEO_FPS)
        print(f"ERROR CODE: {error}, FPS")

    def get_camera_metadata(self):
        if self.capture:
            print(f"Focus value: {self.capture.get(cv2.CAP_PROP_FOCUS)}")
            print(f"Auto focus: {self.capture.get(cv2.CAP_PROP_AUTOFOCUS)}")
            print(f"Image X: {self.capture.get(cv2.CAP_PROP_FRAME_WIDTH)}, Y: {self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)}")
            print(f"Video FPS: {self.capture.get(cv2.CAP_PROP_FPS)}")

    def get_live_frame(self):
        try:
            while True:
                with self.lock:
                    error, encoded_image = cv2.imencode(JPG_EXT, self.image)
                if error:
                    yield b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encoded_image) + b'\r\n'
                else:
                    print(f"ERROR CODE: {error}, imencode")
        except GeneratorExit:
            pass
        finally:
            pass

    def reset_frame_saved(self):
        if int(time.time()) % self.capture_rate != 0:
            self.frame_saved = False

    def reset_counter(self):
        if get_hour() < self.start_hour:
            self.save_index = 0

    def check_save_image(self):
        return not self.frame_saved and self.start_hour <= get_hour() < self.end_hour and int(time.time()) % self.capture_rate == 0

    def save_current_frame(self, image):
        if self.check_save_image():
            error = cv2.imwrite(f'{IMAGE_PATH}/image_{get_day()}_{self.save_index}{JPG_EXT}', image)
            print(f"ERROR CODE: {error}, imwrite")
            self.save_index += 1
            self.frame_saved = True

    def run(self):
        self.running = True
        while self.running:
            error, image = self.capture.read()
            if error:
                with self.lock:
                    self.image = image.copy()
                self.save_current_frame(image)
            else:
                print(f"ERROR CODE: {error}, read")

            self.reset_frame_saved()
            self.reset_counter()
        print("Stopping")

    def set_auto_focus(self):
        self.capture.set(cv2.CAP_PROP_AUTOFOCUS, 1)

    def zero_focus(self):
        self.capture.set(cv2.CAP_PROP_AUTOFOCUS, 0)
        self.capture.set(cv2.CAP_PROP_FOCUS, 0)
        self.capture.set(cv2.CAP_PROP_AUTOFOCUS, 1)

    def update_focus(self, increment):
        self.capture.set(cv2.CAP_PROP_AUTOFOCUS, 0)
        new_focus = self.capture.get(cv2.CAP_PROP_FOCUS) + increment
        self.capture.set(cv2.CAP_PROP_FOCUS, new_focus)

    def increase_focus(self):
        self.update_focus(self.focus_increment)

    def decrease_focus(self):
        self.update_focus(-self.focus_increment)
