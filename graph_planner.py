'''Модуль содержит интерактивный графикопостроитель'''
import tkinter as tk
from math import *

class GraphDrawer:
    def __init__(self, root, width=1000, height=800, center_x=None, center_y=None, scale=10):
        self.root = root
        self.width = width
        self.height = height
        self.center_x = center_x or width // 2
        self.center_y = center_y or height // 2
        self.scale = scale
        self.canvas = tk.Canvas(root, width=width, height=height, bg="white")
        self.canvas.grid(row=0, column=3, rowspan=8)
        self.create_dpsk()

    def create_dpsk(self):
        """Рисуем декартовы оси координат."""
        self.draw_axis(vertical=False, length=self.width)
        self.draw_axis(vertical=True, length=self.height)

    def draw_axis(self, vertical=False, length=500):
        """Рисует ось координат (вертикальную или горизонтальную)."""
        if not vertical:
            shift = (self.width - length) // 2
            self.canvas.create_line(shift, self.center_y, shift + length, self.center_y, arrow='last')
            self.draw_scale(vertical=False, length=length)
        else:
            shift = (self.height - length) // 2
            self.canvas.create_line(self.center_x, shift, self.center_x, shift + length, arrow='first')
            self.draw_scale(vertical=True, length=length)

    def draw_scale(self, vertical=False, length=500):
        """Наносит деления на оси координат."""
        if not vertical:
            x_shift = (self.width - length) // 2
            start = self.center_x - x_shift
            n_positive = (length - start) // self.scale
            n_negative = start // self.scale

            self.canvas.create_text(self.center_x + 12, self.center_y + 12, text=0)
            for i in range(n_positive):
                self.canvas.create_line(self.center_x + i * self.scale, self.center_y - 5, self.center_x + i * self.scale, self.center_y + 5)
                if i != 0:
                    self.canvas.create_text(self.center_x + i * self.scale, self.center_y + 12, text=i)
            for i in range(n_negative):
                self.canvas.create_line(self.center_x - i * self.scale, self.center_y - 5, self.center_x - i * self.scale, self.center_y + 5)
                if i != 0:
                    self.canvas.create_text(self.center_x - i * self.scale, self.center_y + 12, text=i * -1)
        else:
            y_shift = (self.height - length) // 2
            start = self.center_y - y_shift
            n_positive = (length - start) // self.scale
            n_negative = start // self.scale

            for i in range(n_positive):
                self.canvas.create_line(self.center_x + 5, self.center_y + i * self.scale, self.center_x - 5, self.center_y + i * self.scale)
                if i != 0:
                    self.canvas.create_text(self.center_x + 12, self.center_y + i * self.scale, text=i * -1)
            for i in range(n_negative):
                self.canvas.create_line(self.center_x + 5, self.center_y - i * self.scale, self.center_x - 5, self.center_y - i * self.scale)
                if i != 0:
                    self.canvas.create_text(self.center_x + 12, self.center_y - i * self.scale, text=i)



    def draw_function(self, function, a=-4, b=4, color="blue"):
        """Рисует график функции на заданном промежутке."""
        step = 0.1
        x_range = abs(b - a)
        num_steps = int(x_range / step)

        for i in range(num_steps-1):
            x0 = (a + i * step) * self.scale
            y0 = function(a + i * step) * self.scale
            x1 = (a + (i + 1) * step) * self.scale
            y1 = function(a + (i + 1) * step) * self.scale

            self.canvas.create_line(
                self.center_x + x0,
                self.center_y - y0,
                self.center_x + x1,
                self.center_y - y1,
                fill=color
            )

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Графикопостроитель")
    scale = tk.StringVar(value=50) # масштаб
    entry_value = tk.StringVar(value='x**2')
    entry_value1 = tk.StringVar(value='-6')
    entry_value2 = tk.StringVar(value='6')
    
    center_x = 250
    center_y = 200

    def func(x):
        return eval(entry.get())

    def create_graph():
        graph_drawer = GraphDrawer(root, width=500, height=400, center_x=center_x, center_y=center_y, scale=int(spinbox.get()))
        graph_drawer.draw_function(func, a=int(entry1.get()), b=int(entry2.get()), color="green")

    # spinbox для изменения масштаба
    spinbox = tk.Spinbox(from_=1.0, to=100.0, command=create_graph, textvariable=scale)
    spinbox.grid(row=0, column=0, columnspan=3)

    def move_center(c):
        '''Функция перемещает центр.'''
        global center_y, center_x
        if c == 'down':
            center_y += 10
        elif c == 'up':
            center_y -= 10
        elif c == 'left':
            center_x -= 10
        elif c == 'right':
            center_x += 10
        create_graph()

    # поле ввода функции
    entry = tk.Entry(textvariable=entry_value)
    entry.grid(row=1, column=0, columnspan=3)
    
    entry1 = tk.Entry(textvariable=entry_value1, width=5)
    entry1.grid(row=2, column=0)

    entry2 = tk.Entry(textvariable=entry_value2, width=5)
    entry2.grid(row=2, column=2)

    # кнопка для рисование графика
    btn = tk.Button(text="Рисовать",width=15, command=create_graph)
    btn.grid(row=3, column=0, columnspan=3)

    create_graph()

    # легенда
    label = tk.Label(text='Для перемещения\n начала координат\n используйте \n клавиши\n Down \n Up \n Left \n Right', relief="ridge")
    label.grid(row=7, column=0, columnspan=3)

    # обработка событий
    root.bind("<Down>", lambda x: move_center('down'))
    root.bind("<Up>", lambda x: move_center('up'))
    root.bind("<Left>", lambda x: move_center('left'))
    root.bind("<Right>", lambda x: move_center('right'))

    btn_up = tk.Button(text="Up", width=5, command=lambda: move_center('up'))
    btn_up.grid(row=4, column=1)
    btn_down = tk.Button(text="Down", width=5, command=lambda: move_center('down'))
    btn_down.grid(row=6, column=1)
    btn_right = tk.Button(text="Right", width=5, command=lambda: move_center('right'))
    btn_right.grid(row=5, column=2)
    btn_left = tk.Button(text="Left", width=5, command=lambda: move_center('left'))
    btn_left.grid(row=5, column=0)
    

    root.mainloop()
