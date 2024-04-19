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
    # seconds
    capture_rate = 6
    capture_saved = False
    save_index = 0

    start_hour = 3
    end_hour = 22

    capture = None
    image = None
    lock = None
    running = True


    def __init__(self):
        self.capture = cv2.VideoCapture(-1, cv2.CAP_V4L2)

        self.capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.WIDTH)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.HEIGHT)
        self.capture.set(cv2.CAP_PROP_FPS, 20)
        # Focus must be in increments of 25
        # Get video devices: v4l2-ctl --list-devices
        # Get device formats: v4l2-ctl -d /dev/video0 --list-formats-ext
        # self.capture.set(cv2.CAP_PROP_FOCUS, 10) 
        # self.capture.set(cv2.CAP_PROP_AUTOFOCUS, True)
        print("Focus value: ", self.capture.get(cv2.CAP_PROP_FOCUS))
        print("Auto focus: ", self.capture.get(cv2.CAP_PROP_AUTOFOCUS))

        width = int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = self.capture.get(cv2.CAP_PROP_FPS)

        print(width, height, fps)

        self.lock = threading.Lock()
        threading.Thread.__init__(self, daemon=True)
        # self.start()

    def __del__(self):
        self.running = False
        self.capture.release()

    def save_image(self, image):
        # date_string = time.strftime("%m_%d_%H_%M_%S")
        cv2.imwrite(f'{IMAGE_PATH}/image_{self.save_index}.jpg', image)
        self.save_index += 1

    def run(self):
        while self.running:
            ret, image = self.capture.read()
            if ret:
                with self.lock:
                    self.image = image.copy()
                if not self.capture_saved and self.start_hour <= int(time.strftime("%H")) < self.end_hour and int(time.time()) % self.capture_rate == 0:
                    self.save_image(image)
                    self.capture_saved = True
                if int(time.time()) % self.capture_rate != 0:
                    self.capture_saved = False

    def get_current_frame(self):
        with self.lock:
            return self.image

    def set_auto_focus(self):
        self.capture.set(cv2.CAP_PROP_AUTOFOCUS, 1)

    def increase_focus(self):
        print(self.capture.get(cv2.CAP_PROP_FOCUS))
        self.capture.set(cv2.CAP_PROP_AUTOFOCUS, 0)
        current_focus = self.capture.get(cv2.CAP_PROP_FOCUS)
        current_focus += 5
        self.capture.set(cv2.CAP_PROP_FOCUS, current_focus)
        print(self.capture.get(cv2.CAP_PROP_FOCUS))

    def decrease_focus(self):
        print(self.capture.get(cv2.CAP_PROP_FOCUS))
        self.capture.set(cv2.CAP_PROP_AUTOFOCUS, 0)
        current_focus = self.capture.get(cv2.CAP_PROP_FOCUS)
        current_focus -= 5
        self.capture.set(cv2.CAP_PROP_FOCUS, current_focus)
        print(self.capture.get(cv2.CAP_PROP_FOCUS))
