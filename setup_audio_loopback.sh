#!/usr/bin/env bash
set -euo pipefail

# Creates a virtual microphone sink (works with PulseAudio and with
# PipeWire's pulse-compatibility layer, which is the Raspberry Pi OS
# Bookworm default) that apps can pick as an audio input device.
# Usage: ./setup_audio_loopback.sh [sink_name]

SINK_NAME="${1:-VirtualMic}"

sudo apt-get update
sudo apt-get install -y ffmpeg pulseaudio-utils

mkdir -p ~/.config/systemd/user
cat > ~/.config/systemd/user/webcam-simulator-audio-sink.service <<EOF
[Unit]
Description=Virtual microphone sink for webcam-simulator

[Service]
Type=oneshot
RemainAfterExit=yes
ExecStart=/usr/bin/pactl load-module module-null-sink sink_name=${SINK_NAME} sink_properties=device.description=${SINK_NAME}
ExecStop=/usr/bin/pactl unload-module module-null-sink

[Install]
WantedBy=default.target
EOF

systemctl --user daemon-reload
systemctl --user enable --now webcam-simulator-audio-sink.service

echo "Virtual mic ready. Pick '${SINK_NAME} Monitor' as the input device in your app."
pactl list short sinks
