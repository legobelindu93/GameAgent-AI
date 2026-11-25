"""Offline image analysis using OpenCV; no desktop input or game hooks."""
from pathlib import Path

def match_template(image, template, threshold=0.8):
    import cv2
    if not 0 <= threshold <= 1:
        raise ValueError("Invalid threshold")
    frame = cv2.imread(str(Path(image)), cv2.IMREAD_GRAYSCALE)
    pattern = cv2.imread(str(Path(template)), cv2.IMREAD_GRAYSCALE)
    if frame is None or pattern is None:
        raise ValueError("Unreadable image")
    h,w = pattern.shape
    if h > frame.shape[0] or w > frame.shape[1]:
        raise ValueError("Template larger than image")
    if float(pattern.std()) < 1e-6:
        raise ValueError("Constant template")
    result = cv2.matchTemplate(frame, pattern, cv2.TM_CCOEFF_NORMED)
    _, score, _, (x,y) = cv2.minMaxLoc(result)
    return {"found": bool(score >= threshold), "confidence": float(score), "box": [x,y,w,h]}
