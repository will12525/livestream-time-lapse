import cv2
import time
import threading

# 30 frames per second * 60 seconds in a minute * 6.3333 minutes = 11400 frames
# 68400 seconds between 3 and 22 / 11400 frames = 1 frame capture every 6 seconds

IMAGE_PATH = "image_output"


def update_time():
    current_time = time.time()
    print(int(time.time())%6)
    if int(time.time()) % 6 == 0:
        print(current_time)


class CameraControl(threading.Thread):
    WIDTH = 1920
    HEIGHT = 1080
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
    capture_saved = False

    def __init__(self):
        threading.Thread.__init__(self, daemon=True)

    def __del__(self):
        self.running = False
        if self.capture:
            self.capture.release()

    def connect_camera(self, camera_bus):
        self.capture = cv2.VideoCapture(camera_bus, cv2.CAP_V4L2)
        self.capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.WIDTH)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.HEIGHT)
        self.capture.set(cv2.CAP_PROP_FPS, self.VIDEO_FPS)

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
                    error, encoded_image = cv2.imencode(".jpg", self.image)
                if error:
                    yield b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encoded_image) + b'\r\n'
        except GeneratorExit:
            pass
        finally:
            pass

    def save_current_frame(self):
        with self.lock:
            cv2.imwrite(f'{IMAGE_PATH}/image_{self.save_index}.jpg', self.image)
        self.save_index += 1

    def check_save_image(self):
        return not self.capture_saved and self.start_hour <= int(time.strftime("%H")) < self.end_hour and int(time.time()) % self.capture_rate == 0

    def run(self):
        self.running = True
        while self.running:
            ret, image = self.capture.read()
            if ret:
                with self.lock:
                    self.image = image.copy()
                if self.check_save_image():
                    self.save_current_frame()
                    self.capture_saved = True
                if int(time.time()) % self.capture_rate != 0:
                    self.capture_saved = False

    def set_auto_focus(self):
        self.capture.set(cv2.CAP_PROP_AUTOFOCUS, 1)

    def update_focus(self, increment):
        self.capture.set(cv2.CAP_PROP_AUTOFOCUS, 0)
        new_focus = self.capture.get(cv2.CAP_PROP_FOCUS) + increment
        self.capture.set(cv2.CAP_PROP_FOCUS, new_focus)

    def increase_focus(self):
        self.update_focus(self.focus_increment)

    def decrease_focus(self):
        self.update_focus(-self.focus_increment)
