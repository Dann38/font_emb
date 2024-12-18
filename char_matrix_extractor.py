from tesseract_reader.bbox.bbox import BBox
from typing import List
import numpy as np


class CharMatrixExtractor():

    @staticmethod
    def matrix_from_bboxes(img: np.array, list_bboxes: List['BBox'], list_char: List['str']):
        char_image_list = []
        #
        for bbox, index_of_char in zip(list_bboxes, range(len(list_char))):
            image_for_current_bbox = np.zeros((bbox.height, bbox.width, 3))
            x_start = bbox.x_top_left
            y_start = bbox.y_top_left

            for height in range(bbox.height):
                
                for width in range(bbox.width):
                    image_for_current_bbox[height][width] = img[y_start+height][x_start+width]

            char_image_list.append((image_for_current_bbox, list_char[index_of_char]))
        
        return char_image_list
        
        
        
        
        
    