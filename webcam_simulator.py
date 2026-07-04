#!/usr/bin/env python3
"""Loop a video file into a v4l2loopback virtual webcam device."""

import argparse
import os
import time

import cv2
import pyfakewebcam


def _schedule_frame_compat(self, frame):
    """Copy of pyfakewebcam.FakeWebcam.schedule_frame using tobytes() instead
    of the ndarray.tostring() call, which NumPy 2.0 removed. The upstream
    project is unmaintained, so this patches around it instead of pinning an
    old NumPy (which has no prebuilt wheel for recent Python versions)."""
    if frame.shape[0] != self._settings.fmt.pix.height:
        raise Exception(
            f"frame height does not match the height of webcam device: "
            f"{self._settings.fmt.pix.height}!={frame.shape[0]}"
        )
    if frame.shape[1] != self._settings.fmt.pix.width:
        raise Exception(
            f"frame width does not match the width of webcam device: "
            f"{self._settings.fmt.pix.width}!={frame.shape[1]}"
        )
    if frame.shape[2] != self._channels:
        raise Exception(
            f"num frame channels does not match the num channels of webcam device: "
            f"{self._channels}!={frame.shape[2]}"
        )

    self._yuv = cv2.cvtColor(frame, cv2.COLOR_RGB2YUV)

    for i in range(self._settings.fmt.pix.height):
        self._buffer[i, ::2] = self._yuv[i, :, 0]
        self._buffer[i, 1::4] = self._yuv[i, ::2, 1]
        self._buffer[i, 3::4] = self._yuv[i, ::2, 2]

    os.write(self._video_device, self._buffer.tobytes())


pyfakewebcam.FakeWebcam.schedule_frame = _schedule_frame_compat


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
