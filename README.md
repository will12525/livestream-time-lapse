# Live Stream Time Lapse

This program provides a livestream from a connected webcam to a flask webpage.

### Application Features
- Collect 11400 images a day and place them in `image_output/`
  - 1 image every 6 seconds
- Generate a 30 fps video with a length of ~6 minutes at the end of each day in `video_output/`
  - Generated using all 11400 images
- Display a live stream from the webcam when a user connects to the webpage

### Hardware
- Webcam: Logitech c920
- RPI 4

# Setup
This application uses ffmpeg and openocv to read the webcam stream and save images.
Flask is used to create a webpage and stream the live webcam data.
### Install packages
The `setup.sh` script will also attempt to install these packages.
```bash
apt update && apt install build-essential cmake pkg-config libjpeg-dev libtiff5-dev libpng-dev \
  libavcodec-dev libavformat-dev libv4l-dev libxvidcore-dev x264 libx264-dev libfontconfig1-dev \
  libcairo2-dev libgdk-pixbuf2.0-dev libpango1.0-dev libgtk2.0-dev libgtk-3-dev libatlas-base-dev \
  gfortran libhdf5-dev libhdf5-103 python3-pyqt5 python3-dev python3-pip python3-venv python3-numpy \
  python3-opencv git libgstreamer-plugins-base1.0-dev libgstreamer1.0-dev libopenexr-dev \
  libtiff-dev libwebp-dev libopencv-dev libssl-dev ffmpeg -y
```

### Setup
Run the setup script to create the systemctl service and cronjob. This will generate a python3 `.venv` for python modules.
```bash
sudo ./setup.sh
```

### Controlling the application
The livestream and image recording features are handled by systemctl.
```bash
sudo systemctl <start|stop|restart> live_webcam.service
```
Compiling images into a timelapse is handled by a cronjob.
```bash
crontab -e
```
