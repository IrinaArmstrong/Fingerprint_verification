from tkinter import *
import ImageTk
from PIL import Image
import cv2 as cv
import skeletize

# Функция инициализации процесса верификации отпечатков
def checkFinger(ref_filename, ver_filename):
    # Загружаем и обрабатываем файл первого отпечатка
    try:
        reference = Image.open(ref_filename)
        print(reference.format, reference.size, reference.mode)
        # Бинаризация
        binary_reference = binarization(reference)
        # Скелетонизация
        skeletize.skeletonization(binary_reference)
        # Выделение особых точек
        characteristic_points_ref = find_characteristic_points(binary_reference)
        characteristic_points_ref = delete_noise_points(characteristic_points_ref)

    except FileNotFoundError:
        print("File for reference not found!")

    # Загружаем и обрабатываем файл второго отпечатка
    try:
        verification = Image.open(ver_filename)
        print(verification.format, verification.size, verification.mode)
        # Бинаризация
        binary_verification = binarization(verification)
        # Скелетонизация
        skeletize.skeletonization(binary_verification)
        # Выделение особых точек
        characteristic_points_verif = find_characteristic_points(binary_verification)
        characteristic_points_verif = delete_noise_points(characteristic_points_verif)

    except FileNotFoundError:
        print("File for verification not found!")

    # Проверка на совпадение особых точек эталонного и проверчяемого изображений
    resulted_points = matching_points(characteristic_points_ref, characteristic_points_verif)
    matched_points = resulted_points[0]
    all_points = resulted_points[1]
    # Процент совпадения = (matched_points /(all_points*1.))*100
    score = (matched_points / all_points) * 100

    # Визуализируем и отрисовываем результаты
    root = Tk()
    root.title("Results of Fingerprints Detector & Verifier")
    window_width = len(binary_verification)
    window_height = len(binary_verification[0])
    C = Canvas(root, width=window_width*2, height=window_height)

    # ref_image = Image.open(ref_filename)
    # ver_image = Image.open(ver_filename)
    # tk_ref_image = ImageTk.PhotoImage(reference)
    # tk_ver_image = ImageTk.PhotoImage(ver_image)
    # ref_image_sprite = C.create_image(len(binary_verification), len(binary_verification[0]), image=tk_ref_image)
    # ver_image_sprite = C.create_image(len(binary_verification), len(binary_verification[0]), image=tk_ver_image)

    # Рисуем сам отпечаток
    for i in range(window_width):
        for j in range(window_height):
            if binary_reference[i][j] == 0:  # Если пиксель закрашен, то рисуем его
                C.create_line([(i, j), (i+1, j+1)])
            if binary_verification[i][j] == 0:  # Если пиксель закрашен, то рисуем его
                C.create_line([(i+window_width+1, j+1), (i+window_width, j)])

    # Для точек ветвления рисуем овалы
    for i in characteristic_points_ref[0]:  # Проходим по точкам ветвления эталонного отпечатка
        C.create_oval([(i[0]-3, i[1]-3), (i[0]+3, i[1]+3)], outline="#ff0000")
    for i in characteristic_points_verif[0]:  # Проходим по точкам ветвления проверяемого отпечатка
        C.create_oval([(i[0]-3+window_width, i[1]-3), (i[0]+3+window_width, i[1]+3)], outline="#ff0000")

    # Для конечных точек рисуем прямоугольники
    for i in characteristic_points_ref[1]:  # Проходим по конечным точкам эталонного отпечатка
        C.create_rectangle([(i[0]-3, i[1]-3), (i[0]+3, i[1]+3)], outline="#0000ff")
    for i in characteristic_points_verif[1]:  # Проходим по конечным точкам проверяемого отпечатка
        C.create_rectangle([(i[0]-3+window_width, i[1]-3), (i[0]+3+window_width, i[1]+3)], outline="#0000ff")

    C.create_text((window_width, window_width*0.95), fill="#009900", text=str(score)+"%", font='Arial,72')

    C.pack()
    root.mainloop()


# Формирование списков точек ветвления и конечных точек
def find_characteristic_points(img):
    x = len(img)
    y = len(img[0])
    branch_points = []  # Точки ветвления
    end_points = []  # Оконечные точки
    for i in range(x):
        for j in range(y):
            if img[i][j] == 0:
                t = check_curr_point(img, i, j)
                if t == 1:  # Если одна точка - окончание (или 2- ?)
                    end_points.append((i, j))
                if t == 3:  # Если три точки - ветвление
                    branch_points.append((i, j))
    return (branch_points, end_points)


# Подсчет количества закрашенных точек в 3х3 окрестности текущей точки
def check_curr_point(img, x, y):
    c = 0
    for i in range(x-1, x+2):
        for j in range(y-1, y+2):
            if img[i][j] == 0:
                c += 1
    return c-1

# Бинаризация изображения
def binarization(img):
    binary_img = []
    for i in range(img.size[0]):  # img.size[0] = 300 (width)
        tmp = []
        for j in range(img.size[1]):  # img.size[1] = 434 (height)
            r, g, b = img.getpixel((i, j))  # Получаем значения пикселей RGB
            p = r * 0.3 + g * 0.59 + b * 0.11
            if p > 128:  # Порог = 128
                p = 1   # Если больше порога, то окрашиваем в белый (пусто)
            else:
                p = 0  # Иначе, пиксель часть контура - окрашиваем в черный
            tmp.append(p)
        binary_img.append(tmp)
    return binary_img

# Векторная постобработка - удаление шумов,
# которые приводят к появлению отростков, распознаваемых как особые точки.
# Для этого производится удаление близко стоящих (10*10) точек ветвления и конечных точек.
def delete_noise_points(r):
    tmp = []  # Для записи точек конечных
    tmp2 = []  # Для записи точек ветвления
    for i in r[1]:  # Точки конечные
        x = range(i[0]-5, i[0]+5)  # Диапазон [-5,+5] = 10
        y = range(i[1]-5, i[1]+5)  # Диапазон [-5,+5] = 10
        for j in r[0]:  # Точки ветвления
            if j[0] in x and j[1] in y:
                tmp.append(i)
                tmp2.append(j)
    return (remove_double(r[0], tmp2), remove_double(r[1], tmp))


# Функция возвращает список элементов, у которых нет одинакового в другом списке
def remove_double(x, y):
    result_points = []
    for i in x:
        unique = True
        for j in y:
            if i == j:
                unique = False
        if unique:
            result_points.append(i)
    for i in y:
        unique = True
        for j in x:
            if i == j:
                unique = False
        if unique:
            result_points.append(i)
    return result_points


# Проверяем совпадение особых точек эталонного и проверчяемого изображений.
# Возвращаем кортеж из совпавший и всех точек.
def matching_points(reference, verification):
    all_points = 0
    matched_points = 0
    for i in verification[0]:  # Проходим по точкам ветвления проверяемого отпечатка
        x = range(i[0]-15, i[0]+15)  # Поиск в диапазоне [-15,+15] = 30
        y = range(i[1]-15, i[1]+15)  # Поиск в диапазоне [-15,+15] = 30
        all_points += 1
        for j in reference[0]:  # Проходим по точкам ветвления эталона
            if j[0] in x and j[1] in y:  # Если точка попала в диапазон, то совпадает
                matched_points += 1
                break

    for i in verification[1]:  # Проходим по конечным точкам проверяемого отпечатка
        x = range(i[0]-15, i[0]+15)  # Поиск в диапазоне [-15,+15] = 30
        y = range(i[1]-15, i[1]+15)  # Поиск в диапазоне [-15,+15] = 30
        all_points += 1
        for j in reference[1]:  # Проходим по конечным точкам эталона
            if j[0] in x and j[1] in y:  # Если точка попала в диапазон, то совпадает
                matched_points += 1
                break

    return (matched_points, all_points)
