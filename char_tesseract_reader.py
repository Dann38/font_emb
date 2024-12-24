from tesseract_reader.bbox.bbox import BBox
from typing import List, Tuple
import numpy as np
from pytesseract import pytesseract
from tesseract_reader import TesseractReader, TesseractReaderConfig, ImageReader


class CharTesseractReader(TesseractReader):
    def __init__(self, conf: TesseractReaderConfig = None):
        super().__init__(conf)
        self.image_reader = ImageReader()

    @staticmethod
    def get_document_height(image: np.ndarray) -> int:
        height = image.shape[0]
        return height

    def read(self, image: np.ndarray) -> Tuple[List[BBox], List[str]]:
        tesseract_bboxes = pytesseract.image_to_boxes(
            config=self.config.get_args_str(),
            image=image)
        # print(tesseract_bboxes)
        doc_height = self.get_document_height(image)
        tesseract_bboxes = tesseract_bboxes.split('\n')
        list_bbox = []
        list_char = []

        def is_bbox(tmp):
            return len(tmp) < 5

        for i in range(len(tesseract_bboxes)):
            temp = tesseract_bboxes[i].split(' ')
            # print(temp)
            if is_bbox(temp):
                continue
            char = temp[0]
            x_top_left = int(temp[1])
            y_top_left = doc_height - int(temp[4])
            width = int(temp[3]) - x_top_left
            height = int(temp[4]) - int(temp[2])
            list_char.append(char)
            list_bbox.append(BBox(x_top_left, y_top_left, width, height))

        return list_bbox, list_char
