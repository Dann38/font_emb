from tesseract_reader.bbox.bbox import BBox
from typing import List
import numpy as np


class CharMatrixExtractor:

    @staticmethod
    def matrix_from_bboxes(img: np.array, list_bboxes: List['BBox'], list_char: List['str']):
        char_image_list = []

        for index_of_char, bbox in enumerate(list_bboxes):
            x_start = bbox.x_top_left
            y_start = bbox.y_top_left
            height = bbox.height
            width = bbox.width

            image_for_current_bbox = img[y_start:y_start + height, x_start:x_start + width]
            char_image_list.append((image_for_current_bbox, list_char[index_of_char]))

        return char_image_list
        
        
        
        
        
    