"""Script to extract text from images using OCR."""

from abc import ABC, abstractmethod
from pathlib import Path

import cv2
import numpy as np
from retinaface import RetinaFace


class BaseFaceRecognition(ABC):
    """Base class for OCR models."""

    @abstractmethod
    def infer(self, impath: Path | str) -> list[dict]:
        """Abstract method to extract text from image."""
        return

    def visualize(self, impath: Path | str, save_path: Path | str | None = None) -> np.ndarray:
        """Abstract method to visualize the extracted text."""
        img = cv2.imread(str(impath))
        results = self.infer(impath)

        for result in results:
            bbox = result["bbox"]
            x0, y0 = bbox["x0y0"]
            x1, y1 = bbox["x1y1"]
            cv2.rectangle(img, (x0, y0), (x1, y1), (0, 0, 0), 3)
            cv2.rectangle(img, (x0, y0), (x1, y1), (0, 0, 255), 2)

            for landmark_name in result["landmarks"]:
                coords = result["landmarks"][landmark_name]
                x, y = int(coords[0]), int(coords[1])
                cv2.circle(img, (int(x), int(y)), 5, (255, 255, 255), 4)
                cv2.circle(img, (int(x), int(y)), 5, (0, 255, 0), 3)

            # eye and mouth landmarks with a line
            eye_coords = result["landmarks"]["left_eye"], result["landmarks"]["right_eye"]
            mouth_coords = result["landmarks"]["mouth_left"], result["landmarks"]["mouth_right"]

            for vector in [eye_coords, mouth_coords]:
                x0, y0 = int(vector[0][0]), int(vector[0][1])
                x1, y1 = int(vector[1][0]), int(vector[1][1])
                cv2.line(
                    img,
                    (int(x0), int(y0)),
                    (int(x1), int(y1)),
                    (255, 255, 255),
                    3,
                )
                cv2.line(
                    img,
                    (int(x0), int(y0)),
                    (int(x1), int(y1)),
                    (0, 255, 0),
                    2,
                )

        if save_path:
            if not isinstance(save_path, Path):
                save_path = Path(save_path)
            cv2.imwrite(str(save_path.with_suffix(".jpg").resolve()), img)
        return img


class RetinaNetWrapper(BaseFaceRecognition):
    """Wrapper class for EasyOCR."""

    def __init__(self) -> None:
        """Initialize EasyOCRWrapper."""
        self.detector = RetinaFace.detect_faces

    def infer(self, impath: Path | str) -> list[dict]:
        """Read text from image."""
        if isinstance(impath, Path):
            impath = str(impath.resolve())
        results = self.detector(impath)

        # reformat the outputs so that it is consistent with the other face models (list of dicts {text, bbox})
        formatted_results = []
        for result in results:
            bbox_xyxy = results[result]["facial_area"]
            landmarks = results[result]["landmarks"]

            x0, y0 = bbox_xyxy[0], bbox_xyxy[1]
            x1, y1 = bbox_xyxy[2], bbox_xyxy[3]

            x_tl, y_tl = int(x0), int(y0)
            x_br, y_br = int(x1), int(y1)

            bbox = {"x0y0": [x_tl, y_tl], "x1y1": [x_br, y_br]}

            formatted_results.append({"landmarks": landmarks, "bbox": bbox})
        return formatted_results


if __name__ == "__main__":
    image_path = "image.png"
    face = RetinaNetWrapper()
    res = face.visualize(str(image_path), save_path="output.jpg")
    print(res)  # noqa: T201
