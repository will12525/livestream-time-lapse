import argparse
import time
import pathlib
import cv2

IMAGE_PATH = "image_output"
VIDEO_PATH = "video_output"
VIDEO_PATH = "image_output"
FPS = 30
DEFAULT_TIMELAPSE_NAME = "Timelapse"

def setup():
    pass

def create_timelapse(output_file):
    jpeg_folder_path = pathlib.Path(IMAGE_PATH).resolve()
    jpeg_file_paths = sorted(jpeg_folder_path.rglob('*.jpg'), key=lambda path: int(path.stem.rsplit("_", 1)[1]))
    height = width = video = None
    fourcc = cv2.VideoWriter_fourcc('a', 'v', 'c', '1')
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
        

if __name__ == '__main__':
    output_file_name = f"{DEFAULT_TIMELAPSE_NAME} - s{int(time.strftime('%Y'))}e{int(time.strftime('%j'))}.mp4"

    setup()

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', "--file_name", type=str)    
    args = parser.parse_args()
    if args.file_name:
        output_file_name = f"{args.file_name} {output_file_name}"

    create_timelapse(f"{VIDEO_PATH}/{output_file_name}")

