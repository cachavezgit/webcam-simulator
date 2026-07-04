#!/usr/bin/env python3
"""Loop a video file into a v4l2loopback virtual webcam device."""

import argparse
import time

import cv2
import pyfakewebcam


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("video", help="Path to the video file to loop")
    parser.add_argument("--device", default="/dev/video10", help="v4l2loopback device node")
    parser.add_argument("--width", type=int, default=1280)
    parser.add_argument("--height", type=int, default=720)
    parser.add_argument("--fps", type=float, default=30.0)
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    cap = cv2.VideoCapture(args.video)
    if not cap.isOpened():
        raise SystemExit(f"Could not open video file: {args.video}")

    camera = pyfakewebcam.FakeWebcam(args.device, args.width, args.height)
    frame_interval = 1.0 / args.fps

    try:
        while True:
            start = time.monotonic()

            ok, frame = cap.read()
            if not ok:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue

            frame = cv2.resize(frame, (args.width, args.height))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            camera.schedule_frame(frame)

            elapsed = time.monotonic() - start
            time.sleep(max(0.0, frame_interval - elapsed))
    except KeyboardInterrupt:
        pass
    finally:
        cap.release()


if __name__ == "__main__":
    main()
