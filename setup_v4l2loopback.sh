#!/usr/bin/env bash
set -euo pipefail

# Installs and loads v4l2loopback, creating a persistent virtual webcam device.
# Usage: ./setup_v4l2loopback.sh [video_nr] [card_label]

VIDEO_NR="${1:-10}"
CARD_LABEL="${2:-VirtualCam}"

sudo apt-get update
sudo apt-get install -y v4l2loopback-dkms v4l-utils

# Load immediately for this session.
sudo modprobe -r v4l2loopback 2>/dev/null || true
sudo modprobe v4l2loopback devices=1 video_nr="${VIDEO_NR}" card_label="${CARD_LABEL}" exclusive_caps=1

# Persist across reboots.
echo "v4l2loopback" | sudo tee /etc/modules-load.d/v4l2loopback.conf > /dev/null
echo "options v4l2loopback devices=1 video_nr=${VIDEO_NR} card_label=\"${CARD_LABEL}\" exclusive_caps=1" \
    | sudo tee /etc/modprobe.d/v4l2loopback.conf > /dev/null

echo "Virtual webcam ready at /dev/video${VIDEO_NR} (${CARD_LABEL})"
v4l2-ctl --device="/dev/video${VIDEO_NR}" --info
