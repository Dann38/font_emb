import random
from PIL import Image, ImageDraw, ImageFont
from string_generator import StringGenerator


class FontGenerator:
    def __init__(self):
        self.fonts = [
            r'C:\Windows\Fonts\Arial.ttf',
            r'C:\Windows\Fonts\Times New Roman.ttf',
            r'C:\Windows\Fonts\Calibri.ttf',
            r'C:\Windows\Fonts\Impact.ttf',
            r'C:\Windows\Fonts\Arial Black.ttf',
            r'C:\Windows\Fonts\Courier New.ttf',
            r'C:\Windows\Fonts\Consolas.ttf',
            r'C:\Windows\Fonts\Cascadia Mono.ttf',
            r'C:\Windows\Fonts\Helvetica.ttf',
            r'C:\Windows\Fonts\Verdana.ttf',
            r'C:\Windows\Fonts\Tahoma.ttf',
            r'C:\Windows\Fonts\Lucida Console.ttf',
            r'C:\Windows\Fonts\Garamond.ttf',
            r'C:\Windows\Fonts\Book Antiqua.ttf',
            r'C:\Windows\Fonts\Cambria.ttf',
            r'C:\Windows\Fonts\Constantia.ttf',
            r'C:\Windows\Fonts\Segoe Script.ttf',
            r'C:\Windows\Fonts\Comic Sans MS.ttf',
            r'C:\Windows\Fonts\Monotype Corsiva.ttf',
            r'C:\Windows\Fonts\Leelawadee UI Semilight.ttf'
        ]


    def create_image_with_text(self, text, font_path, image_size=(200, 100), font_size=40):
        image = Image.new('RGB', image_size, 'white')  # изображение с белым фоном
        draw = ImageDraw.Draw(image)

        font = ImageFont.truetype(font_path, font_size)

        # центрирование
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        position = ((image_size[0] - text_width) // 2, (image_size[1] - text_height) // 2)

        draw.text(position, text, fill='black', font=font)

        return image

    def generate_images(self):
        for i in range(20):
            lang = random.choice(['rus', 'eng'])
            text = StringGenerator.text_generator(lang)
            font_path = random.choice(self.fonts)
            image = self.create_image_with_text(text, font_path)
            image.save(f'dataset/image_{i}.png')


font_generator = FontGenerator()
font_generator.generate_images()
