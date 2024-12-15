
import pytesseract
from tesseract_reader import ImageReader
from tesseract_reader.bbox.bbox import BBox

class SymbolsExtractor:
    
    @staticmethod
    def take_symbols_and_bboxes(filename, lang):
        image_reader = ImageReader()
        string = pytesseract.image_to_boxes(image_reader.read(filename), lang)
        string = string.split('\n')

        return string

