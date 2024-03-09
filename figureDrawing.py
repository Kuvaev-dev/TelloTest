import cv2
import turtle

def draw_contour(contour, img_shape):
    h, w = img_shape
    for i in range(len(contour)):
        x = contour[i][0][0]  # Отримуємо x-координату i-тої точки контуру
        y = contour[i][0][1]  # Отримуємо y-координату i-тої точки контуру

        # Перетворюємо координати
        x = x - w/2  # Переміщуємо x-координату так, щоб центр зображення був в (0,0)
        y = h/2 - y  # Переміщуємо y-координату так, щоб центр зображення був в (0,0), та інвертуємо ось y, оскільки в зображеннях ось y спрямована вниз

        if i == 0:
            turtle.penup()
            turtle.goto(x, y)
            turtle.pendown()
        else:
            turtle.goto(x, y)

def main():
    # Зчитуємо зображення
    img = cv2.imread('figures/square.jpg', cv2.IMREAD_GRAYSCALE)

    # Змінюємо розмір зображення
    img = cv2.resize(img, (200, 200))

    # Застосовуємо розмиття Гаусса
    img = cv2.GaussianBlur(img, (5, 5), 0)

    # Застосовуємо адаптивне порогове значення
    adaptive_thresh = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    # Застосовуємо детектор країв Canny
    edges = cv2.Canny(adaptive_thresh, 50, 150)

    # Знаходимо контури
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # Відображаємо контури за допомогою turtle
    turtle.speed(1)
    for contour in contours:
        draw_contour(contour, img.shape)  # використовуємо contour замість cv2.convexHull(contour)
    
    turtle.done()
    turtle.mainloop()  # додаємо цей рядок

if __name__ == "__main__":
    main()
