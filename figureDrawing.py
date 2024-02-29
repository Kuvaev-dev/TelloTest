import cv2  # Бібліотека для завантаження зображення
from djitellopy import Tello   # Tello Drone

# Створення об'єкту Tello
my_drone = Tello()

# Піключення до дрону
my_drone.connect()

# Вказуємо шлях до зображення
image_path = input("Пожалуйста, введите путь к изображению: ")

# Завантаження зображення
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

# Для отримання бінарного зображення задаємо порогове значення
_, binary_image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)

# Знаходимо контури на бнарному зображенні
contours, _ = cv2.findContours(binary_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Проходимо по усім контурам
for contour in contours:
    # Приводимо контур до масиву точок
    points = contour.reshape(-1, 2)
    
    # Проходимо по усім точкам
    for point in points:
        # Задаємо напрям для малювання
        my_drone.move_up(point[0])  # Початковий підйом
        my_drone.move_forward(point[0])
        my_drone.move_right(point[1])

# Приземляємо дрон після малювання
my_drone.land()
