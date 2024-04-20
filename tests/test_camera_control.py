from unittest import TestCase
from camera_control import CameraControl

from . import patch_time_time, patch_time_strftime


class TestCameraControl(TestCase):
    def setup(self):
        pass


class TestCameraControlSaveImage(TestCameraControl):

    def test_is_capture_time_mock_time_in_range_capture_saved_true(self):
        camera_control = CameraControl()
        patch_time_time(self, camera_control.capture_rate)
        camera_control.frame_saved = True
        for i in range(camera_control.start_hour, camera_control.end_hour):
            patch_time_strftime(self, i)
            assert not camera_control.check_save_image()

    def test_is_capture_time_mock_time_in_range(self):
        camera_control = CameraControl()
        patch_time_time(self, camera_control.capture_rate)
        for i in range(camera_control.start_hour, camera_control.end_hour):
            patch_time_strftime(self, i)
            assert camera_control.check_save_image()

    def test_is_capture_time_mock_time_lower_boundary(self):
        camera_control = CameraControl()
        patch_time_time(self, camera_control.capture_rate)
        for i in range(0, camera_control.start_hour):
            patch_time_strftime(self, i)
            assert not camera_control.check_save_image()

    def test_is_capture_time_mock_time_lower_boundary_saved_true(self):
        camera_control = CameraControl()
        patch_time_time(self, camera_control.capture_rate)
        camera_control.frame_saved = True
        for i in range(0, camera_control.start_hour):
            patch_time_strftime(self, i)
            assert not camera_control.check_save_image()

    def test_is_capture_time_mock_time_upper_boundary(self):
        camera_control = CameraControl()
        patch_time_time(self, camera_control.capture_rate)
        for i in range(camera_control.end_hour, 24):
            patch_time_strftime(self, i)
            assert not camera_control.check_save_image()

    def test_is_capture_time_mock_time_upper_boundary_saved_true(self):
        camera_control = CameraControl()
        patch_time_time(self, camera_control.capture_rate)
        camera_control.frame_saved = True
        for i in range(camera_control.end_hour, 24):
            patch_time_strftime(self, i)
            assert not camera_control.check_save_image()


class TestCameraControlGeneral(TestCameraControl):
    # def test_update_time(self):
    #     while True:
    #         update_time()
    def test_reset_counter(self):
        camera_control = CameraControl()
        camera_control.save_index = 1
        patch_time_time(self, camera_control.capture_rate)
        for i in range(camera_control.start_hour, camera_control.end_hour):
            patch_time_strftime(self, i)
            camera_control.reset_counter()
            assert camera_control.save_index == 1

    def test_reset_counter_lower_boundary(self):
        camera_control = CameraControl()
        patch_time_time(self, camera_control.capture_rate)
        for i in range(0, camera_control.start_hour):
            camera_control.save_index = 1
            patch_time_strftime(self, i)
            camera_control.reset_counter()
            assert camera_control.save_index == 0

    def test_reset_counter_upper_boundary(self):
        camera_control = CameraControl()
        patch_time_time(self, camera_control.capture_rate)
        for i in range(camera_control.end_hour, 24):
            camera_control.save_index = 1
            patch_time_strftime(self, i)
            camera_control.reset_counter()
            assert camera_control.save_index == 1

    def test_percent_out(self):
        my_list = [0] * 120

        for index, i in enumerate(my_list):
            int((index / len(my_list)) * 100)
            print(f"{int((index/len(my_list)) * 100)}%")

    def test_increase_focus(self):
        camera_control = CameraControl()
        camera_control.increase_focus()

    def test_decrease_focus(self):
        camera_control = CameraControl()
        camera_control.decrease_focus()
