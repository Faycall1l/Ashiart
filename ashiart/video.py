"""Optional video and webcam input. Requires opencv-python.

Install with the extra: pip install ashiart[video]
"""

from __future__ import annotations

from collections.abc import Iterator

from PIL import Image, ImageOps


def _require_cv2():
    """Import cv2 or explain the missing optional dependency."""
    try:
        import cv2
    except ImportError as error:
        raise ValueError(
            "Video input needs OpenCV: pip install ashiart[video]"
        ) from error
    return cv2


def iter_video_frames(
    path: str, max_frames: int | None = None
) -> Iterator[tuple[Image.Image, int]]:
    """Yield (RGB frame, duration_ms) pairs from a video file.

    Args:
        path (str): Local video file path.
        max_frames (int or None): Frame cap; None reads to the end.

    Yields:
        tuple: (PIL.Image, int) per frame.
    """
    cv2 = _require_cv2()
    capture = cv2.VideoCapture(path)
    try:
        fps = capture.get(cv2.CAP_PROP_FPS) or 25.0
        duration = int(1000 / fps)
        count = 0
        while max_frames is None or count < max_frames:
            ok, frame = capture.read()
            if not ok:
                break
            yield Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)), duration
            count += 1
    finally:
        capture.release()


def iter_webcam_frames(index: int = 0, mirror: bool = True) -> Iterator[Image.Image]:
    """Yield RGB frames from a webcam until the generator is closed.

    Args:
        index (int): Camera device index.
        mirror (bool): Flip horizontally for a selfie view.

    Yields:
        PIL.Image: Live RGB frames.
    """
    cv2 = _require_cv2()
    capture = cv2.VideoCapture(index)
    try:
        while True:
            ok, frame = capture.read()
            if not ok:
                break
            image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            yield image if not mirror else ImageOps.mirror(image)
    finally:
        capture.release()
