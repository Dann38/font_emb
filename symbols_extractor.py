from PIL import Image
import pytesseract


class symbols_extractor():
    @staticmethod
    def take_symbols_and_bboxes(filename, lang):
        string = pytesseract.image_to_boxes(Image.open(filename), lang)
        string = string.split('\n')
        return string

