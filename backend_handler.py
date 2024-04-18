import threading
import cv2
import numpy as np
import pathlib
import random
from camera_control import CameraControl


class Controller(threading.Thread):
    camera_control = None

    def __init__(self):
        self.camera_control = CameraControl()
        self.camera_control.start()
        threading.Thread.__init__(self, daemon=True)

    def run(self):
        pass

    def get_live_frame(self):
        while self.camera_control:
            output_frame = self.camera_control.get_current_frame()
            if output_frame is None:
                continue

            (flag, encodedImage) = cv2.imencode(".jpg", output_frame)
            if flag:
                yield b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n'

    def decrease_focus(self):
        if self.camera_control:
            self.camera_control.decrease_focus()

    def increase_focus(self):
        if self.camera_control:
            self.camera_control.increase_focus()

    def set_auto_focus(self):
        if self.camera_control:
            self.camera_control.set_auto_focus()

