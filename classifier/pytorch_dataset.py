import os
import cv2
import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader
from PIL import Image
from matplotlib import pyplot as plt


class CharImageDataset(Dataset):
    def __init__(self, img_dir, transform=None, target_transform=None):
        self.img_dir = img_dir
        self.labels = ['0', '1']
        self.counts = [len(os.listdir(os.path.join(self.img_dir, label))) for label in self.labels]
        self.count = sum(self.counts)
        self.transform = transform
        self.target_transform = target_transform

    def __len__(self):
        return self.count

    def __getitem__(self, idx):
        label, i = self.__get_label_and_i_from_idx(idx)
        img_path = os.path.join(self.img_dir, label, f"image_{i}.png")
        image = Image.open(img_path)
        image_array = np.array(image)

        if self.transform:
            image_array = self.transform(image_array)
        if self.target_transform:
            label = self.target_transform(label)
        return image_array, label

    def __get_label_and_i_from_idx(self, idx):
        k = 0
        while (idx - self.counts[k]) >= 0:
            idx -= self.counts[k]
            k += 1
        return self.labels[k], idx

@staticmethod
def label_to_vec(text):
    return torch.Tensor([float(text[0])])

@staticmethod
def image_to_gray(image):
    grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) / 255.0
    return torch.Tensor(grayscale_image).unsqueeze(0)  # размерность канала


# Проверка
# dataset = CharImageDataset("dataset/", transform=image_to_gray, target_transform=label_to_vec)
#
# image, label = dataset[3]
# print(label)
# print(image[0][0])
# plt.imshow(image[0])  # [] - для выделения канала, тут только ч/б
# plt.axis('off')  # Скрываем оси
# plt.show()