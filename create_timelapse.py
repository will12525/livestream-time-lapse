import argparse
import time
import pathlib
import cv2
import shutil
import requests

IMAGE_PATH = "image_output"
VIDEO_PATH = "video_output"
FPS = 30
DEFAULT_TIMELAPSE_NAME = "Timelapse"


def setup():
    image_path = pathlib.Path(IMAGE_PATH).resolve()
    if not image_path.exists():
        image_path.mkdir(exist_ok=True)
    video_path = pathlib.Path(VIDEO_PATH).resolve()
    if not video_path.exists():
        video_path.mkdir(exist_ok=True)
    print("Finished setup")

def teardown():
    shutil.rmtree(IMAGE_PATH)


def create_timelapse(output_file):
    jpeg_folder_path = pathlib.Path(IMAGE_PATH).resolve()
    jpeg_file_paths = sorted(jpeg_folder_path.rglob('*.jpg'), key=lambda path: int(path.stem.rsplit("_", 1)[1]))
    height = width = video = None
    fourcc = cv2.VideoWriter_fourcc('a', 'v', 'c', '1')
    print(f"Starting build, writing file to {output_file}")
    for index, image_path in enumerate(jpeg_file_paths):
        image = cv2.imread(str(image_path))
        if height is None or width is None:
            height, width, layers = image.shape
        if video is None and height and width:
            video = cv2.VideoWriter(output_file, fourcc, FPS, (width, height))
        if video:
            video.write(image)

    cv2.destroyAllWindows()
    if video:
        video.release()
    print("Timelapse complete")


def upload_file(url, file_name):
    response = requests.post(url, files={'file': open(file_name, 'rb')})
    print(response)


if __name__ == '__main__':
    output_file_name = f"{DEFAULT_TIMELAPSE_NAME} - s{int(time.strftime('%Y'))}e{int(time.strftime('%j'))}.mp4"

    setup()

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', "--file_name", type=str)    
    parser.add_argument('-u', "--url", type=str)    
    args = parser.parse_args()

    if args.file_name:
        output_file_name = f"{args.file_name} {output_file_name}"
    create_timelapse(f"{VIDEO_PATH}/{output_file_name}")
    
    if args.url:
        print(args.url)
        upload_file(args.url, f"{VIDEO_PATH}/{output_file_name}")

#    teardown()
