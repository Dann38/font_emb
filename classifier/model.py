import cv2
import numpy as np
import torch
import torch.nn as nn
from torch import optim
from torch.utils.data import Dataset, DataLoader
from pytorch_dataset import CharImageDataset, label_to_vec, image_to_gray
from pil_font_generator import FontGenerator
from PIL import Image


class CharCNNClassifier(nn.Module):
    def __init__(self):
        super(CharCNNClassifier, self).__init__()

        # Сверточные слои
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=16, kernel_size=3, stride=1, padding=1)
        self.conv2 = nn.Conv2d(in_channels=16, out_channels=32, kernel_size=3, stride=1, padding=1)

        # Максимальный пулинг
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)

        # Полносвязные слои
        self.fc1 = nn.Linear(32 * 15 * 60, 128)  # Обновлено
        self.fc2 = nn.Linear(128, 1)  # Выходной вектор длины 1

        # Функция активации
        self.relu = nn.ReLU()

    def forward(self, x):
        # Применяем свертки и пулинг
        x = self.pool(self.relu(self.conv1(x)))  # (batch_size, 16, 30, 120)
        x = self.pool(self.relu(self.conv2(x)))  # (batch_size, 32, 15, 60)

        # Выравниваем тензор для полносвязного слоя
        x = x.view(x.size(0), -1)  # (batch_size, 32 * 15 * 60)

        # Применяем полносвязные слои
        x = self.relu(self.fc1(x))  # (batch_size, 128)
        x = self.fc2(x)  # (batch_size, 1)

        return x


dataset = CharImageDataset("dataset/", transform=image_to_gray, target_transform=label_to_vec)

num_epochs = 20

# model = CharCNNClassifier()
#
# example_batch_x = torch.stack([dataset[i][0] for i in range(2)])  # (2, 1, 60, 240)
# example_batch_y = torch.stack([dataset[i][1] for i in range(2)])  # (2, 1)
#
# # проверка входных данных
# print("example_batch_x shape:", example_batch_x.shape)  # (2, 1, 60, 240)
# print("example_batch_y shape:", example_batch_y.shape)  # (2, 1)
#
# output = model(example_batch_x)
#
# # проверка выходных данных
# print("Output shape:", output.shape)  # (2, 1)
# print("Output:", output)
# print("Labels:", example_batch_y)


model = CharCNNClassifier()
criterion = nn.BCEWithLogitsLoss() # функция потерь
optimizer = optim.Adam(model.parameters(), lr=0.001)
train = DataLoader(dataset, batch_size=128, shuffle=True)
for epoch in range(num_epochs):
    model.train()  # Переводим модель в режим обучения
    running_loss = 0.0

    for i, (inputs, targets) in enumerate(train):
        # Обнуляем градиенты
        optimizer.zero_grad()

        # Прямой проход
        outputs = model(inputs)

        # Вычисление потерь
        loss = criterion(outputs, targets)

        # Обратное распространение и обновление весов
        loss.backward()
        optimizer.step()

        # Суммируем потери для вывода
        running_loss += loss.item()

        # Выводим статистику каждые 10 батчей
        if i % 10 == 9:
            print(f"Epoch [{epoch + 1}/{num_epochs}], Batch [{i + 1}/{len(train)}], Loss: {running_loss / 10:.4f}")
            running_loss = 0.0


# Проверка работы модели

def classifier(model, char):
    gray_image = image_to_gray(char)
    data = gray_image.unsqueeze(0)
    rez = model(data)
    return torch.mean(rez, 0)


def interpretation_class(v):
    if v < 0.5:
        print("Шрифты разные")
    else:
        print("Шрифты одинаковые")


font_generator = FontGenerator()
font_generator.generate_images(1, answer=1, style=True)

image_path = 'dataset/image_1.png'
image = Image.open(image_path)

image_array = np.array(image)

# проверка размерности
# print("image_array shape:", image_array.shape)  # (60, 240, 3)

v = classifier(model, image_array)
print(v)
interpretation_class(v)