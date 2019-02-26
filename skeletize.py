# Функция инициализации процесса скелетонизации
def skeletonization(img):
    width = len(img)
    height = len(img[0])
    del_count = 1  # Счетчик удаленных пикселей

    # Проводим процедуру скелетонизации до тех пор,
    # пока можно очистить/закрасить хоть один пиксель изображения
    while del_count != 0:
        # Удаление пикселя по основному набору шаблонов
        del_count = delete_maintemp(img, width, height)
        if del_count:
            # Удаление пикселя по дополнительному набору шаблонов, для устранения шумов
            delete_addtemp(img, width, height)

#  Удаление пикселя по основному набору шаблонов
def delete_maintemp(img, w, h):
    del_count = 0
    for i in range(1, h-1):
        for j in range(1, w-1):
            if img[j][i] == 0:
                if init_check_maintemp(img, j, i):
                    img[j][i] = 1
                    del_count += 1
    return del_count


# Удаление пикселя по дополнительному набору шаблонов, для устранения шумов
def delete_addtemp(img, w, h):
    for i in range(1, h-1):
        for j in range(1, w-1):
            if img[j][i] == 0:
                if init_check_addtemp(img, j, i):
                    img[j][i] = 1




# Выделяем для каждого пикселя область 3х3 и
# проводим проверку на соответствие одному из основных шаблонов
def init_check_maintemp(img, x, y):
    ROI = []
    for i in range(y-1, y+2):
        for j in range(x-1, x+2):
            ROI.append(img[j][i])
    return check_main_template(ROI)


# Выделяем для каждого пикселя область 3х3 и
# проводим проверку на соответствие одному из дополнительных шаблонов
def init_check_addtemp(img, x, y):
    ROI = []
    for i in range(y-1, y+2):
        for j in range(x-1, x+2):
            ROI.append(img[j][i])
    return check_additional_template(ROI)


# Проверка на соответствие области 3х3 одному из дополнительных шаблонов
def check_additional_template(a):
    t = [[1, 1, 1, 1, 0, 1, 1, 1, 1],

         [1, 1, 1, 1, 0, 1, 1, 0, 0],
         [1, 1, 1, 0, 0, 1, 0, 1, 1],
         [0, 0, 1, 1, 0, 1, 1, 1, 1],
         [1, 1, 0, 1, 0, 0, 1, 1, 1],

         [1, 1, 1, 1, 0, 1, 0, 0, 1],
         [0, 1, 1, 0, 0, 1, 1, 1, 1],
         [1, 0, 0, 1, 0, 1, 1, 1, 1],
         [1, 1, 1, 1, 0, 0, 1, 1, 0],

         [1, 1, 1, 1, 0, 1, 0, 0, 0],
         [0, 1, 1, 0, 0, 1, 0, 1, 1],
         [0, 0, 0, 1, 0, 1, 1, 1, 1],
         [1, 1, 0, 1, 0, 0, 1, 1, 0]]
    for i in t:
        if a == i:
            return True

# Проверка на соответствие области 3х3 одному из основных шаблонов
def check_main_template(a):
    templ_1 = [1, 1, 0, 0, 1, 0]
    templ_2 = [1, 1, 1, 0, 0, 0]
    templ_3 = [0, 1, 0, 0, 1, 1]
    templ_4 = [0, 0, 0, 1, 1, 1]
    templ_5 = [1, 1, 1, 0, 0, 0, 0]
    templ_6 = [1, 0, 1, 0, 0, 1, 0]
    templ_7 = [0, 0, 0, 0, 1, 1, 1]
    templ_8 = [0, 1, 0, 0, 1, 0, 1]

    t = [a[1], a[2], a[3], a[4], a[5], a[7]]
    if t == templ_1:
        return True
    t = [a[0], a[1], a[3], a[4], a[5], a[7]]
    if t == templ_2:
        return True
    t = [a[1], a[3], a[4], a[5], a[6], a[7]]
    if t == templ_3:
        return True
    t = [a[1], a[3], a[4], a[5], a[7], a[8]]
    if t == templ_4:
        return True
    t = [a[0], a[1], a[2], a[3], a[4], a[5], a[7]]
    if t == templ_5:
        return True
    t = [a[0], a[1], a[3], a[4], a[5], a[6], a[7]]
    if t == templ_6:
        return True
    t = [a[1], a[3], a[4], a[5], a[6], a[7], a[8]]
    if t == templ_7:
        return True
    t = [a[1], a[2], a[3], a[4], a[5], a[7], a[8]]
    if t == templ_8:
        return True
