import os
import pytesseract
from symbols_extractor import SymbolsExtractor
from tesseract_reader import ImageReader, TesseractReader, TesseractReaderConfig
from char_tesseract_reader import CharTesseractReader

if __name__ == '__main__':
    # Image path /example_img/img_1.jpeg
    path_project = os.path.abspath(os.path.join(os.getcwd(), "."))
    path_img = os.path.join(path_project, 'example_img', "img_1.jpeg")

    # Objects
    image_reader = ImageReader()
    tesseract_config = TesseractReaderConfig()
    tesseract_reader = TesseractReader(tesseract_config)

    img = image_reader.read(path_img)

    # print(tesseract_reader.read(img))
    char_tesseract_reader = CharTesseractReader(tesseract_config)
    print(char_tesseract_reader.read(img))








