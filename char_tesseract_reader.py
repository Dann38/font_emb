from tesseract_reader.bbox.bbox import BBox
from typing import List, Tuple
import numpy as np
from pytesseract import pytesseract
from tesseract_reader import TesseractReader, TesseractReaderConfig


class CharTesseractReader(TesseractReader):
    def __init__(self, conf: TesseractReaderConfig = None):
        super().__init__(conf)

    def read(self, image: np.ndarray) -> Tuple[List[BBox], List[str]]:
        tesseract_bboxes = pytesseract.image_to_boxes(
            config=self.config.get_args_str(),
            image=image,
            output_type=pytesseract.Output.DICT)
        tesseract_bboxes = tesseract_bboxes.split('\n')
        list_bbox = []
        list_char = []


        for i in range(len(tesseract_bboxes)):
            temp = tesseract_bboxes[i].split(' ')
            if len(temp) < 5: continue
            char = temp[0]
            x = int(temp[1])
            y = int(temp[2])
            w = int(temp[3]) - x
            h = int(temp[4]) - y
            list_char.append(char)
            list_bbox.append(BBox(x, y, w, h))

        return list_bbox, list_char
