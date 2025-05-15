import tkinter as tk
from tkinter import filedialog, font, messagebox, Menu, Scrollbar

class TextEditor(tk.Tk):
    def __init__(self):
        super().__init__()

        # Настройка окна приложения
        self.title("Текстовый редактор")
        self.geometry('800x600')

        # Текущий открытый файл (None изначально)
        self.current_filename = None

        # Главное меню
        menubar = tk.Menu(self)

        # Меню "Файл"
        file_menu = tk.Menu(menubar, tearoff=False)
        file_menu.add_command(label="Открыть", accelerator="Ctrl+O", command=self.open_file)
        file_menu.add_command(label="Сохранить", accelerator="Ctrl+S", command=self.save_file)
        file_menu.add_command(label="Сохранить как...", accelerator="Ctrl+Shift+S", command=self.save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label="Закрыть файл", accelerator="Ctrl+W", command=self.clear_editor)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", accelerator="Alt+F4", command=self.quit)
        menubar.add_cascade(label="Файл", menu=file_menu)

        # Меню "Правка"
        edit_menu = tk.Menu(menubar, tearoff=False)
        edit_menu.add_command(label="Отменить", accelerator="Ctrl+Z", command=lambda: self.text_area.event_generate("<<Undo>>"))
        edit_menu.add_command(label="Вернуть", accelerator="Ctrl+Y", command=lambda: self.text_area.event_generate("<<Redo>>"))
        edit_menu.add_separator()
        edit_menu.add_command(label="Вырезать", accelerator="Ctrl+X", command=lambda: self.text_area.event_generate("<<Cut>>"))
        edit_menu.add_command(label="Копировать", accelerator="Ctrl+C", command=lambda: self.text_area.event_generate("<<Copy>>"))
        edit_menu.add_command(label="Вставить", accelerator="Ctrl+V", command=lambda: self.text_area.event_generate("<<Paste>>"))
        edit_menu.add_separator()
        edit_menu.add_command(label="Удалить", accelerator="Del", command=lambda: self.text_area.event_generate("<<Delete>>"))
        edit_menu.add_command(label="Выделить всё", accelerator="Ctrl+A", command=lambda: self.text_area.tag_add("sel", "1.0", tk.END))
        edit_menu.add_separator()
        edit_menu.add_command(label="Найти", accelerator="Ctrl+F", command=self.find_text)
        edit_menu.add_command(label="Заменить", accelerator="Ctrl+H", command=self.replace_text)
        menubar.add_cascade(label="Правка", menu=edit_menu)

        # Меню "Формат"
        format_menu = tk.Menu(menubar, tearoff=False)
        format_menu.add_command(label="Шрифт", command=self.select_font)
        menubar.add_cascade(label="Формат", menu=format_menu)

        # Меню "Вид"
        view_menu = tk.Menu(menubar, tearoff=False)
        view_menu.add_command(label="Масштаб увеличить", accelerator="+", command=self.increase_zoom)
        view_menu.add_command(label="Масштаб уменьшить", accelerator="-", command=self.decrease_zoom)
        menubar.add_cascade(label="Вид", menu=view_menu)

        self.config(menu=menubar)

        # Главный фрейм для контейнера
        main_frame = tk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Панель для ввода текста
        self.text_area = tk.Text(main_frame, wrap=tk.NONE, undo=True)
        self.text_area.grid(row=0, column=0, sticky="nsew")

        # Горизонтальный и вертикальный скроллеры
        hscroll = Scrollbar(main_frame, orient=tk.HORIZONTAL, command=self.text_area.xview)
        vscroll = Scrollbar(main_frame, orient=tk.VERTICAL, command=self.text_area.yview)
        self.text_area['xscrollcommand'] = hscroll.set
        self.text_area['yscrollcommand'] = vscroll.set
        hscroll.grid(row=1, column=0, sticky="ew")
        vscroll.grid(row=0, column=1, sticky="ns")

        # Глобально настраиваем Grid-стратегию растяжения
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        # Привязываем обработчики клавиш через ключевые коды
        self.bind_all('<KeyPress>', self.handle_keypress)

    def handle_keypress(self, event):
        """Универсальный обработчик горячих клавиш."""
        # Получаем код нажатой клавиши
        key_code = event.keycode
        ctrl_pressed = event.state & 0x4 != 0  # Проверяем наличие модификатора Control

        # Определение конкретных клавиш через их числовые коды
        if ctrl_pressed:
            if key_code == 79:  # Код клавиши 'O'
                self.open_file()
            elif key_code == 83:  # Код клавиши 'S'
                self.save_file()
            elif key_code == 88:  # Код клавиши 'X' (Вырезать)
                self.text_area.event_generate("<<Cut>>")
            elif key_code == 67:  # Код клавиши 'C' (Копировать)
                self.text_area.event_generate("<<Copy>>")
            elif key_code == 86:  # Код клавиши 'V' (Вставить)
                self.text_area.event_generate("<<Paste>>")
            elif key_code == 90:  # Код клавиши 'Z' (Отменить)
                self.text_area.event_generate("<<Undo>>")
            elif key_code == 89:  # Код клавиши 'Y' (Вернуть)
                self.text_area.event_generate("<<Redo>>")
            elif key_code == 65:  # Код клавиши 'A' (Выделить всё)
                self.text_area.tag_add("sel", "1.0", tk.END)
            elif key_code == 70:  # Код клавиши 'F' (Поиск)
                self.find_text()
            elif key_code == 72:  # Код клавиши 'H' (Заменить)
                self.replace_text()

    def update_title(self):
        """Обновляет заголовок окна с именем файла."""
        title = "Текстовый редактор"
        if self.current_filename:
            title += f" — {self.current_filename.split('/')[-1].split('\\')[-1]}"
        self.title(title)

    def open_file(self):
        """Открытие файла."""
        filename = filedialog.askopenfilename(filetypes=(("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")))
        if not filename:
            return
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            self.text_area.delete('1.0', tk.END)
            self.text_area.insert(tk.END, content)
        self.current_filename = filename
        self.update_title()

    def save_file(self):
        """Сохранение файла (только если файл уже открыт)."""
        if self.current_filename is None:
            self.save_as_file()
        else:
            with open(self.current_filename, 'w', encoding='utf-8') as f:
                text_to_save = self.text_area.get('1.0', tk.END)
                f.write(text_to_save)

    def save_as_file(self):
        """Сохранение файла с выбором имени файла."""
        initial_name = ""
        if self.current_filename:
            initial_name = self.current_filename.split("/")[-1].split("\\")[-1]
        filename = filedialog.asksaveasfilename(initialfile=initial_name, defaultextension=".txt",
                                               filetypes=(("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")))
        if not filename:
            return
        with open(filename, 'w', encoding='utf-8') as f:
            text_to_save = self.text_area.get('1.0', tk.END)
            f.write(text_to_save)
        self.current_filename = filename
        self.update_title()

    def clear_editor(self):
        """Очистка текущего состояния редактора."""
        self.text_area.delete('1.0', tk.END)
        self.current_filename = None
        self.update_title()

    def find_text(self):
        """Диалог поиска текста."""
        search_dialog = tk.Toplevel(self)
        search_dialog.title("Найти")
        label = tk.Label(search_dialog, text="Что искать:")
        entry = tk.Entry(search_dialog)
        button_find = tk.Button(search_dialog, text="Искать", command=lambda: self.search(entry.get()))
        label.grid(row=0, column=0)
        entry.grid(row=0, column=1)
        button_find.grid(row=1, columnspan=2)

    def replace_text(self):
        """Диалог замены текста."""
        replace_dialog = tk.Toplevel(self)
        replace_dialog.title("Заменить")
        label_find = tk.Label(replace_dialog, text="Что заменить:")
        entry_find = tk.Entry(replace_dialog)
        label_replace = tk.Label(replace_dialog, text="На что заменить:")
        entry_replace = tk.Entry(replace_dialog)
        button_replace = tk.Button(replace_dialog, text="Заменить", command=lambda: self.replace(entry_find.get(), entry_replace.get()))
        label_find.grid(row=0, column=0)
        entry_find.grid(row=0, column=1)
        label_replace.grid(row=1, column=0)
        entry_replace.grid(row=1, column=1)
        button_replace.grid(row=2, columnspan=2)

    def search(self, pattern):
        """Осуществляет поиск заданного фрагмента текста."""
        pos = self.text_area.search(pattern, "insert", stopindex=tk.END)
        if pos:
            endpos = f"{pos}+{len(pattern)}c"
            self.text_area.tag_remove("search", "1.0", tk.END)
            self.text_area.tag_add("search", pos, endpos)
            self.text_area.see(pos)
            self.text_area.focus_set()
            self.text_area.mark_set("insert", endpos)
        else:
            messagebox.showinfo("Поиск", "Текст не найден.")

    def replace(self, old_pattern, new_pattern):
        """Реализация функции замены текста."""
        pos = self.text_area.search(old_pattern, "insert", stopindex=tk.END)
        if pos:
            endpos = f"{pos}+{len(old_pattern)}c"
            self.text_area.delete(pos, endpos)
            self.text_area.insert(pos, new_pattern)
            self.text_area.see(pos)
            self.text_area.focus_set()
            self.text_area.mark_set("insert", pos + f"+{len(new_pattern)}c")
        else:
            messagebox.showinfo("Замена", "Текст не найден.")

    def select_font(self):
        """Выбор шрифта."""
        self.tk.call("tk", "fontchooser", "configure", "-font", self.text_area["font"], "-command",
                     self.register(self.font_changed))
        self.tk.call("tk", "fontchooser", "show")

    def font_changed(self, new_font):
        """Изменяет шрифт в области редактирования."""
        self.text_area.configure(font=new_font)

    def increase_zoom(self):
        """Увеличивает размер шрифта."""
        current_font = font.Font(font=self.text_area.cget("font"))
        size = current_font.actual()['size']
        self.text_area.configure(font=(current_font.actual()['family'], size + 2))

    def decrease_zoom(self):
        """Уменьшает размер шрифта."""
        current_font = font.Font(font=self.text_area.cget("font"))
        size = current_font.actual()['size']
        if size > 2:
            self.text_area.configure(font=(current_font.actual()['family'], size - 2))


if __name__ == "__main__":
    editor = TextEditor()
    editor.mainloop()