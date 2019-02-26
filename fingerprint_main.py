from tkinter import *
from tkinter import filedialog
import pycorrelate
import points

def start():
    points.checkFinger(inPut.get(), outPut.get())

def openRef(event):
    options = {}
    options['defaultextension'] = ''
    options['filetypes'] = [('text files', '.txt')]
    options['initialdir'] = 'C:\\'
    options['parent'] = root
    options['title'] = 'Open Input File'

    # Диалоговое окно для открытия файла, возвращает имя файла, который должен быть открыт
    input = filedialog.askopenfile()
    if input:
        inPut.set(input.name)

def openVer(event):
    options = {}
    options['defaultextension'] = ''
    options['filetypes'] = [('text files', '.txt')]
    options['initialdir'] = 'C:\\'
    options['parent'] = root
    options['title'] = 'Open Output File'

    # Диалоговое окно для открытия файла, возвращает имя файла, который должен быть открыт
    output = filedialog.askopenfile()
    if output:
        outPut.set(output.name)

# Создаем окно
global root
root = Tk()
root.title("Fingerprints Detector & Verifier")
w = root.winfo_screenwidth()  # Ширина экрана
h = root.winfo_screenheight()  # Высота экрана
w = w//2  # Середина экрана
h = h//2
w = w - 200  # Смещение от середины
h = h - 200
root.geometry('+{}+{}'.format(w, h))

global inPut
global outPut
global autoGraph
inPut = StringVar()
inPut.set('')
outPut = StringVar()
outPut.set('')
autoGraph = StringVar()
autoGraph.set('')

inEntry = Entry(root, textvariable=inPut)  #
outEntry = Entry(root, textvariable=outPut)  #

getInFile = Button(root, text='Open Reference')  #
getOutFile = Button(root, text='Open Verificable')  #

getInFile.bind('<1>', openRef)
getOutFile.bind('<1>', openVer)

sign = Button(root, text='Start', command=start)

# Позиционирование элементов
inEntry.grid(row=0, column=0, padx=10, pady=10)
outEntry.grid(row=1, column=0, padx=10, pady=10)

getInFile.grid(row=0, column=1, padx=10, pady=10)
getOutFile.grid(row=1, column=1, padx=10, pady=10)

sign.grid(row=3, column=1, padx=10, pady=10)

# Отображаем окно
root.mainloop()