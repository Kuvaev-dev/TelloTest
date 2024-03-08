import cv2 # Зчитування зображення та створення полігону
import numpy as np # Робота з масивом пікселів
from djitellopy import Tello # Дрон
import time # Для затримок дрону

# Створюємо об'єкт дрона
drone = tello.Tello()

# Підключаємося до дрона
drone.connect()

# Отримуємо та виводимо рівень батареї
battery = drone.get_battery()
print(f"Рівень батареї: {battery}%")

# Злітаємо
drone.takeoff()

# Чекаємо 5 секунд для стабілізації
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

# Зберігаємо початкову позицію
start_x, start_y = 0, 0

# Проходимо по всіх точках полігона
for point in polygon:
    x, y = point[0]
    # Рухаємося до наступної точки
    drone.move_right(x - start_x)
    drone.move_up(y - start_y)
    # Оновлюємо поточну позицію
    start_x, start_y = x, y

# Повертаємося до початкової позиції
drone.move_left(start_x)
drone.move_down(start_y)

# Чекаємо 5 секунд
time.sleep(5)

# Сідаємо
drone.land()
