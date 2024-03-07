# Імпортуємо необхідні бібліотеки
import cv2 # для роботи з зображеннями
import numpy as np # для роботи з масивами
import tello # для роботи з дроном
import time # для роботи з часом

# Створюємо об'єкт дрона
drone = tello.Tello()

# Підключаємося до дрона
drone.connect()

# Отримуємо рівень батареї
battery = drone.get_battery()

# Виводимо рівень батареї
print(f"Рівень батареї: {battery}%")

# Злітаємо
drone.takeoff()

# Чекаємо 5 секунд
time.sleep(5)

# Прохання користувача ввести шлях до зображення
image_path = input("Введіть шлях до зображення: ")

# Зчитуємо зображення
image = cv2.imread(image_path)

# Перетворюємо зображення в відтінки сірого
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Знаходимо контури на зображенні
contours, hierarchy = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Сортуємо контури за площею в порядку спадання
contours = sorted(contours, key=cv2.contourArea, reverse=True)

# Беремо перший контур (найбільший)
contour = contours[0]

# Апроксимуємо контур за допомогою полігона
epsilon = 0.01 * cv2.arcLength(contour, True)
polygon = cv2.approxPolyDP(contour, epsilon, True)

# Знаходимо кількість вершин полігона
vertices = len(polygon)

# В залежності від кількості вершин полігона, задаємо напрямок польоту дрона
if vertices == 3:
    # Трикутник - летимо вліво
    drone.move_left(100)
elif vertices == 4:
    # Прямокутник - летимо вправо
    drone.move_right(100)
elif vertices == 5:
    # П'ятикутник - летимо вгору
    drone.move_up(100)
elif vertices == 6:
    # Шестикутник - летимо вниз
    drone.move_down(100)
else:
    # Невизначена фігура - летимо назад
    drone.move_back(100)

# Чекаємо 5 секунд
time.sleep(5)

# Сідаємо
drone.land()
