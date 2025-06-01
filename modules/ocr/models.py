"""Script to extract text from images using OCR."""

from abc import ABC, abstractmethod
from pathlib import Path

import cv2
import numpy as np
from easyocr import Reader
from torch.cuda import is_available


class BaseOCR(ABC):
    """Base class for OCR models."""

    @abstractmethod
    def infer(self, impath: Path | str) -> list[dict]:
        """Abstract method to extract text from image."""
        pass  # noqa: PIE790

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
            cv2.putText(img, result["text"], (x0, y0 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 3)
            cv2.putText(img, result["text"], (x0, y0 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        if save_path:
            if not isinstance(save_path, Path):
                save_path = Path(save_path)
            cv2.imwrite(str(save_path.with_suffix(".jpg").resolve()), img)
        return img


class EasyOCRWrapper(BaseOCR):
    """Wrapper class for EasyOCR."""

    def __init__(self) -> None:
        """Initialize EasyOCRWrapper."""
        self.reader = Reader(["en"], gpu=is_available())

    def infer(self, impath: Path | str) -> list[dict]:
        """Read text from image."""
        if isinstance(impath, Path):
            impath = str(impath.resolve())
        results = self.reader.readtext(impath)

        # reformat the outputs so that it is consistent with the other OCR models (list of dicts {text, bbox})
        formatted_results = []
        for result in results:
            bbox, text, score = result

            """ bbox has x1y1, x2y2, x3y3, x4y4 format.
            Find top-left and bottom-right coordinates by using min/max operations"""

            bbox = np.array(bbox)
            x_tl, y_tl = np.min(bbox, axis=0)
            x_br, y_br = np.max(bbox, axis=0)
            bbox = {"x0y0": [x_tl, y_tl], "x1y1": [x_br, y_br]}

            formatted_results.append({"text": text, "bbox": bbox})
        return formatted_results


if __name__ == "__main__":
    image_path = "image.png"
    ocr = EasyOCRWrapper()
    res = ocr.visualize(str(image_path))
    print(res)  # noqa: T201
