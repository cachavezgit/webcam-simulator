#!/usr/bin/env python3
"""Loop a video file's audio track into a virtual microphone sink."""

import argparse
import subprocess


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("video", help="Path to the video file whose audio track will be looped")
    parser.add_argument("--sink", default="VirtualMic", help="PulseAudio/PipeWire sink to play into")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    cmd = [
        "ffmpeg",
        "-stream_loop", "-1",
        "-re",
        "-i", args.video,
        "-vn",
        "-f", "pulse",
        "-device", args.sink,
        "webcam-simulator-audio",
    ]

    try:
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
