import tkinter
from tkinter import font
from tkinter import *
from tkinter import ttk
import tkcap
from PIL import Image
import os
from string_generator import StringGenerator
import itertools

root = tkinter.Tk()
root.title("Fonts")

font_names = ['Arial', 'Times New Roman', 'Calibri', 'Impact', 'Arial Black', 'Courier New', 'Consolas', 'Cascadia Mono', 'Helvetica', 'Verdana', 'Tahoma', 'Lucida Console', 'Garamond', 'Book Antiqua', 'Cambria', 'Constantia', 'Segoe Script', 'Comic Sans MS', 'Monotype Corsiva', 'Leelawadee UI Semilight']
fonts = sorted(font_names)
# print(fonts)
# print(len(fonts))
weight = ['normal', 'bold']
slant = ['roman', 'italic']
underline = [True, False]
overstrike = [True, False]
background = ['yellow', 'green', 'red', 'blue', None]

combinations = itertools.product(weight, slant, underline, overstrike, background, fonts)


def generate_file_name(name, w, s, u, o, b, i):

    file_name = f'training_images/{name}_{w}_{s}_'
    file_name += 'u_' if underline else 'nu_'
    file_name += 'o_' if overstrike else 'no_'
    file_name += b + '_' if b else ''

    return file_name + str(i) + '_eng' + '.png'


i = 0
for combo in combinations:
    w, s, u, o, b, name = combo
    text = StringGenerator.text_generator('eng')
    font = tkinter.font.Font(family=name, size=18, weight=w, slant=s, underline=u, overstrike=o)
    label = tkinter.Label(root, text=text, font=font, background=b, foreground='black')
    label.pack(pady=10)

    root.update()  # обновляется окно чтобы отобразить текст

    file_name = generate_file_name(name, w, s, u, o, b, i)

    cap = tkcap.CAP(root)
    cap.capture(file_name)

    image = Image.open(file_name)
    image_crop = image.crop((0, 28, 120, 83))
    os.remove(file_name)
    image_crop.save(file_name, quality=95)

    label.destroy()  # удаляет текст

    i += 1


