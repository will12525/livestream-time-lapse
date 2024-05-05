#!/bin/bash

WORKSPACE=$(pwd)

SERVICE="live_webcam.service"
LINUX_SERVICE_DIR="/etc/systemd/system/"
PY_VENV="${WORKSPACE}/.venv"
PY_VENV_ACTIVATE="${PY_VENV}/bin/activate"
PY_REQ="${WORKSPACE}/requirements.txt"

IMAGE_OUTPUT="${WORKSPACE}/image_output"
VIDEO_OUTPUT="${WORKSPACE}/video_output"

if [ "$EUID" -ne 0 ]; then
  echo "Please run as root"
  exit
fi

echo "Installing packages"
apt update && apt install build-essential cmake pkg-config libjpeg-dev libtiff5-dev libpng-dev libavcodec-dev libavformat-dev libv4l-dev libxvidcore-dev x264 libx264-dev libfontconfig1-dev libcairo2-dev libgdk-pixbuf2.0-dev libpango1.0-dev libgtk2.0-dev libgtk-3-dev libatlas-base-dev gfortran libhdf5-dev libhdf5-103 python3-pyqt5 python3-dev python3-pip python3-venv python3-numpy python3-opencv git libgstreamer-plugins-base1.0-dev libgstreamer1.0-dev libopenexr-dev libtiff-dev libwebp-dev libopencv-dev libssl-dev ffmpeg -y

echo "Creating python venv"
python3 -m venv "${PY_VENV}"
# shellcheck source=.venv
source "${PY_VENV_ACTIVATE}"
pip install -r "${PY_REQ}"
chown -R "${SUDO_USER}":"${SUDO_USER}" "${PY_VENV}"

echo "Setting up folders"
install -d -o "${SUDO_USER}" -g "${SUDO_USER}" -m 0755 "${IMAGE_OUTPUT}"
install -d -o "${SUDO_USER}" -g "${SUDO_USER}" -m 0755 "${VIDEO_OUTPUT}"

echo "Installing services"
sed -i "s,INSTALL_USR,${SUDO_USER},g" "${SERVICE}"
sed -i "s,INSTALL_DIR,${WORKSPACE},g" "${SERVICE}"
cp "${SERVICE}" "${LINUX_SERVICE_DIR}"
systemctl daemon-reload
systemctl enable "${SERVICE}"
systemctl start "${SERVICE}"

echo "Installing cron"
crontab -u "${SUDO_USER}" -l > timelapse_cron
echo "22 0 * * * cd ${WORKSPACE} && ./run.sh --compress && rm -rf ${IMAGE_OUTPUT} && mkdir ${IMAGE_OUTPUT}" >> timelapse_cron
crontab -u "${SUDO_USER}" timelapse_cron
rm timelapse_cron
