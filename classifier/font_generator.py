import tkinter
from tkinter import font
from tkinter import *
from tkinter import ttk
import tkcap
from PIL import Image
import os
from string_generator import StringGenerator

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

i = 0
for name in fonts:
    for w in weight:
        for s in slant:
            for u in underline:
                for o in overstrike:
                    for b in background:

                        text = StringGenerator.text_generator('eng')

                        font = tkinter.font.Font(family=name, size=18, weight=w, slant=s, underline=u, overstrike=o)
                        label = tkinter.Label(root, text=text, font=font, background=b, foreground='black')
                        label.pack(pady=10)

                        root.update() # обновляется окно чтобы отобразить текст

                        cap = tkcap.CAP(root)
                        file_name = f'training_images/{name}_{w}_{s}_'
                        if underline:
                            file_name += 'u_'
                        else:
                            file_name += 'nu_'

                        if overstrike:
                            file_name += 'o_'
                        else:
                            file_name += 'no_'

                        if b:
                            file_name += b + '_'

                        cap.capture(file_name + str(i) + '_eng' + '.png')

                        image = Image.open(file_name + str(i) + '_eng' + '.png')
                        image_crop = image.crop((0, 28, 120, 83))
                        os.remove(file_name + str(i) + '_eng' + '.png')
                        image_crop.save(file_name + str(i) + '_eng' + '.png', quality=95)

                        label.destroy() # удаляет текст

                        i += 1


