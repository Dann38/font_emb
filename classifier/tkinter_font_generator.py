import random
import tkinter
from tkinter import font
from tkinter import *
import tkcap
from PIL import Image
import os
from string_generator import StringGenerator
import itertools
import time

class Generator:

    def __init__(self):

        self.font_names = ['Arial', 'Times New Roman', 'Calibri', 'Impact', 'Arial Black', 'Courier New', 'Consolas', 'Cascadia Mono', 'Helvetica', 'Verdana', 'Tahoma', 'Lucida Console', 'Garamond', 'Book Antiqua', 'Cambria', 'Constantia', 'Segoe Script', 'Comic Sans MS', 'Monotype Corsiva', 'Leelawadee UI Semilight']
        self.fonts = sorted(self.font_names)
        self.weight = ['normal', 'bold']
        self.slant = ['roman', 'italic']
        self.underline = [True, False]
        self.overstrike = [True, False]
        self.background = ['yellow', 'green', 'red', 'blue', None]

    def generate_random_style(self):
        style = []
        style.append(random.randint(0, len(self.fonts) - 1))

        for i in range(4):
            style.append(random.randint(0, 1))

        style.append(random.randint(0, len(self.background) - 1))
        return style


    def return_array(self, style, text):
        first_image = (self.generate_random_style(), StringGenerator.text_generator('eng'))
        second_image = (first_image[0] if style else self.generate_random_style(), first_image[1] if text else StringGenerator.text_generator('eng'))
        return first_image, second_image, 1 if style else 0


    def draw_font(self, index, style = False, text = False):
        first_image, second_image, result = self.return_array(style, text)
        images = [first_image, second_image]
        print(images)
        for i, image in enumerate(images):
            root = tkinter.Tk()
            root.title("Fonts")

            name, w, s, u, o, b = image[0]
            name, w, s, u, o, b = self.fonts[name], self.weight[w], self.slant[s], self.underline[u], self.overstrike[o], self.background[b]
            text = image[1]
            print(name, w, s, u, o, b)
            font = tkinter.font.Font(family=name, size=18, weight=w, slant=s, underline=u, overstrike=o)
            label = tkinter.Label(root, text=text, font=font, background=b, foreground='black')
            label.pack(pady=10)

            root.update()

            file_name = os.path.join(os.getcwd(), 'dataset', f'img{index}_{i}.jpeg')

            time.sleep(0.1)

            cap = tkcap.CAP(root)
            cap.capture(file_name)

            image = Image.open(file_name)
            image_crop = image.crop((0, 28, 120, 83))
            os.remove(file_name)
            image_crop.save(file_name, quality=95)

            time.sleep(0.1)

            root.destroy()


        with open('dataset/result.txt', 'a') as file:
            file.write(str(result) + '\n')


    def generate_file_name(self, name, w, s, u, o, b, i):
        file_name = f'training_images/{name}_{w}_{s}_'
        file_name += 'u_' if u else 'nu_'
        file_name += 'o_' if o else 'no_'
        file_name += b + '_' if b else ''

        return file_name + str(i) + '_eng' + '.png'

    # Генерация всех комбинаций шрифтов
    def generate_random_font(self):

        root = tkinter.Tk()
        root.title("Fonts")

        combinations = itertools.product(self.weight, self.slant, self.underline, self.overstrike, self.background, self.fonts)

        i = 0
        for combo in combinations:
            w, s, u, o, b, name = combo
            text = StringGenerator.text_generator('eng')
            font = tkinter.font.Font(family=name, size=18, weight=w, slant=s, underline=u, overstrike=o)
            label = tkinter.Label(root, text=text, font=font, background=b, foreground='black')
            label.pack(pady=10)

            root.update()  # обновляется окно чтобы отобразить текст

            file_name = self.generate_file_name(name, w, s, u, o, b, i)

            cap = tkcap.CAP(root)
            cap.capture(file_name)

            image = Image.open(file_name)
            image_crop = image.crop((0, 28, 120, 83))
            os.remove(file_name)
            image_crop.save(file_name, quality=95)

            label.destroy()  # удаляет текст

            i += 1

# Generator = Generator()
# for i in range(100):
#     if i < 30:
#         Generator.draw_font(i)
#     elif i < 60:
#         Generator.draw_font(i, style=True)
#     else:
#         Generator.draw_font(i, text=True)
