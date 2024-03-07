import cv2  # Бібліотека для завантаження зображення
from djitellopy import Tello   # Tello Drone

# Створення об'єкту Tello
my_drone = Tello()

# Піключення до дрону
my_drone.connect()
my_drone.takeoff()

# Вказуємо шлях до зображення
image_path = input("Будь-ласка, введіть шлях до зображення: ")

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
        my_drone.move_forward(point[0])  # Переміщення вперед
        my_drone.move_right(point[1])  # Переміщення вправо

# Приземляємо дрон після малюванняна на поаткову точку
my_drone.move_back(0)
my_drone.move_left(0)
my_drone.land()
