import cv2  
from djitellopy import Tello   

def main():
    # Створення об'єкту Tello
    my_drone = Tello()

    # Підключення до дрону
    if not my_drone.connect():
        print("Помилка підключення до дрону.")
        return

    if not my_drone.takeoff():
        print("Помилка взльоту дрону.")
        return

    # Вказуємо шлях до зображення
    image_path = input("Будь-ласка, введіть шлях до зображення: ")

    # Завантаження зображення
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        print("Не вдалося завантажити зображення.")
        return

    # Для отримання бінарного зображення задаємо порогове значення
    _, binary_image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)

    # Знаходимо контури на бінарному зображенні
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Проходимо по усім контурам
    for contour in contours:
        # Знаходимо центр маси контуру
        M = cv2.moments(contour)
        if M["m00"] != 0:
            # m00 - нульовий момент (область контуру), m19 - перший момент контуру за віссю Х (сума значень пікселів, помножених на їх відстань від вісі Y)
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            
            # Переміщення дрона до центру маси контуру з плавною зміною висоти
            if not my_drone.go_xyz_speed(cx - image.shape[1] // 2, cy - image.shape[0] // 2, 0, 30):
                print("Помилка переміщення дрона.")
                return
            
            # Затримка між кадрами для стабілізації дрону
            cv2.waitKey(500)

    # Зупинка дрона перед приземленням
    if not my_drone.send_rc_control(0, 0, 0, 0):
        print("Помилка управління дроном.")
        return

    # Затримка перед приземленням для стабілізації
    cv2.waitKey(2000)

    # Приземлення дрона
    if not my_drone.land():
        print("Помилка приземлення дрона.")
        return

    # Затримка перед завершенням програми
    cv2.waitKey(5000)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
