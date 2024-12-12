import os
from PIL import Image
import pytesseract
from symbols_extractor import symbols_extractor
from tesseract_reader import ImageReader, TesseractReader, TesseractReaderConfig

if __name__ == '__main__':
    # Image path /example_img/img_1.jpeg
    path_project = os.path.abspath(os.path.join(os.getcwd(), "."))
    path_img = os.path.join(path_project, 'example_img', "1_img.png")

    # Objects
    image_reader = ImageReader()
    tesseract_config = TesseractReaderConfig()
    tesseract_reader = TesseractReader(tesseract_config)

    img = image_reader.read(path_img)

    print(tesseract_reader.read(img))

    list_bbox, list_matrix = tesseract_reader.read(img)

    for matrix in list_matrix:
        print(matrix)

    print(len(list_matrix))

    print(symbols_extractor.take_symbols_and_bboxes(path_img, 'eng'))






