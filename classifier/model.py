import torch
import torch.nn as nn
import torchvision
import torch.nn.functional as F


num_epochs = 5
num_classes = 20
batch_size = 100
learning_rate = 0.01
DATA_PATH = ''


class CharCNNClassifier(nn.Module):
    def __init__(self):
        super(CharCNNClassifier, self).__init__()

        # Сверточные слои
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=16, kernel_size=3, stride=1, padding=1)
        self.conv2 = nn.Conv2d(in_channels=16, out_channels=32, kernel_size=3, stride=1, padding=1)

        # Максимальный пулинг
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)

        # Полносвязные слои
        self.fc1 = nn.Linear(32 * 10 * 7, 128)  # После пулинга размер изображения уменьшается
        self.fc2 = nn.Linear(128, 3)  # Выходной вектор длины 3

        # Функция активации
        self.relu = nn.ReLU()

    def forward(self, x):
        # Применяем свертки и пулинг
        x = self.pool(self.relu(self.conv1(x)))  # Размер: (batch_size, 16, 20, 15) <- размер уменьшился в 2 раза
        x = self.pool(self.relu(self.conv2(x)))  # Размер: (batch_size, 32, 10, 7) <- размер уменьшился в 2 раза

        # Выравниваем тензор для полносвязного слоя
        x = x.view(x.size(0), -1)  # Размер: (batch_size, 32 * 10 * 7)

        # Применяем полносвязные слои
        x = self.relu(self.fc1(x))  # Размер: (batch_size, 128)
        x = self.fc2(x)  # Размер: (batch_size, 3)

        return x