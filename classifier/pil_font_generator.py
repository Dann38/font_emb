import os.path
import random
from PIL import Image, ImageDraw, ImageFont
from string_generator import StringGenerator


class FontGenerator:
    def __init__(self):
        self.fonts = [
            r'fonts\\arial.ttf',  # Arial
            r'fonts\\times.ttf'  # Times New Roman
            r'fonts\\calibri.ttf',  # Calibri
            r'fonts\\impact.ttf',  # Impact
            r'fonts\\ariblk.ttf',  # Arial Black
            r'fonts\\cour.ttf',  # Courier New
            r'fonts\\consola.ttf',  # Consolas
            r'fonts\\CascadiaMono.ttf',  # Cascadis Mono
            r'fonts\\verdana.ttf',  # Verdana
            r'fonts\\tahoma.ttf',  # Tahoma
            r'fonts\\lucon.ttf',  # Lucida Console
            r'fonts\\GARA.ttf',  # Garamond
            r'fonts\\BKANT.ttf',  # Book Antiqua
            r'fonts\\cambria.ttc',  # Cambria
            r'fonts\\constan.ttf',  # Constantia
            r'fonts\\segoesc.ttf',  # Segoe Script
            r'fonts\\comic.ttf',  # Comic Sans MS
            r'fonts\\MTCORSVA.ttf',  # Monotype Corsiva

        ]
        self.image_size = (120, 60)
        self.font_size = 40
        self.intervals = [
            (-10, 10),  # отклонение по ширине
            (-20, 10)  # отклонение по высоте
        ]

    def random_position_with_constraints(self):
        # разделяем интервалы для ширины (x) и высоты (y)
        x_interval, y_interval = self.intervals

        # генерация случайной позиции по ширине
        x = random.randint(x_interval[0], x_interval[1])

        # генерация случайной позиции по высоте
        y = random.randint(y_interval[0], y_interval[1])

        return (x, y)

    def draw_font(self, text, font_path, image_size, font_size):
        image = Image.new('RGB', image_size, 'white')  # изображение с белым фоном
        draw = ImageDraw.Draw(image)

        font = ImageFont.truetype(font_path, font_size)

        position = self.random_position_with_constraints()

        draw.text(position, text, fill='black', font=font)

        return image

    def generate_images(self, index, answer, style=False, same_text=False):
        lang = random.choice(['rus', 'eng'])
        # одинаковый шрифт
        if style:
            font_path = random.choice(self.fonts)
            font_name = os.path.basename(font_path).split('.')[0]
            images = []
            for i in range(2):
                text = StringGenerator.text_generator(lang)
                images.append(self.draw_font(text, font_path, self.image_size, self.font_size))
        # одинаковый текст
        elif same_text:
            text = StringGenerator.text_generator(lang)
            images = []
            for i in range(2):
                font_path = random.choice(self.fonts)
                font_name = os.path.basename(font_path).split('.')[0]
                images.append(self.draw_font(text, font_path, self.image_size, self.font_size))
        # все разное
        else:
            images = []
            for i in range(2):
                font_path = random.choice(self.fonts)
                font_name = os.path.basename(font_path).split('.')[0]
                text = StringGenerator.text_generator(lang)
                images.append(self.draw_font(text, font_path, self.image_size, self.font_size))
        final_image = Image.new('RGB', (images[0].width + images[1].width, images[1].height))
        final_image.paste(images[0], (0, 0))
        final_image.paste(images[1], (images[0].width, 0))
        final_image.save(f'dataset/{answer}/image_{index}.png')


font_generator = FontGenerator()
for i in range(10000):
    if i < 2500:
        font_generator.generate_images(i, answer=0)
    elif i < 5000:
        font_generator.generate_images(i, answer=1, style=True)
    else:
        font_generator.generate_images(i, answer=0, same_text=True)
