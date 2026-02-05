"""
Простой блокнот на Tkinter с темной темой.
"""

import tkinter as tk
from tkinter import filedialog, messagebox
import os


class Notepad:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Простой блокнот")
        self.root.geometry("600x400")

        self.bg_color = "#2b2b2b"
        self.fg_color = "#ffffff"
        self.text_bg = "#3c3f41"
        self.text_fg = "#bbbbbb"
        self.menu_bg = "#3c3f41"
        self.menu_fg = "#bbbbbb"
        self.button_bg = "#505050"
        self.button_fg = "#ffffff"

        self.current_file = None

        self.create_widgets()

    def create_widgets(self):
        self.root.configure(bg=self.bg_color)

        menubar = tk.Menu(self.root, bg=self.menu_bg, fg=self.menu_fg)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0, bg=self.menu_bg, fg=self.menu_fg)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Новый", command=self.new_file)
        file_menu.add_command(label="Открыть", command=self.open_file)
        file_menu.add_command(label="Сохранить", command=self.save_file)
        file_menu.add_command(label="Сохранить как", command=self.save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.root.quit)

        edit_menu = tk.Menu(menubar, tearoff=0, bg=self.menu_bg, fg=self.menu_fg)
        menubar.add_cascade(label="Правка", menu=edit_menu)
        edit_menu.add_command(label="Очистить", command=self.clear_text)

        help_menu = tk.Menu(menubar, tearoff=0, bg=self.menu_bg, fg=self.menu_fg)
        menubar.add_cascade(label="Справка", menu=help_menu)
        help_menu.add_command(label="О программе", command=self.show_about)

        toolbar = tk.Frame(self.root, bg=self.bg_color)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        tk.Button(toolbar, text="Новый", command=self.new_file,
                 bg=self.button_bg, fg=self.button_fg).pack(side=tk.LEFT, padx=2, pady=2)
        tk.Button(toolbar, text="Открыть", command=self.open_file,
                 bg=self.button_bg, fg=self.button_fg).pack(side=tk.LEFT, padx=2, pady=2)
        tk.Button(toolbar, text="Сохранить", command=self.save_file,
                 bg=self.button_bg, fg=self.button_fg).pack(side=tk.LEFT, padx=2, pady=2)
        tk.Button(toolbar, text="Очистить", command=self.clear_text,
                 bg=self.button_bg, fg=self.button_fg).pack(side=tk.LEFT, padx=2, pady=2)

        text_frame = tk.Frame(self.root, bg=self.bg_color)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        scrollbar = tk.Scrollbar(text_frame, bg=self.button_bg)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.text_area = tk.Text(
            text_frame,
            wrap=tk.WORD,
            yscrollcommand=scrollbar.set,
            bg=self.text_bg,
            fg=self.text_fg,
            font=("Arial", 12),
            insertbackground=self.fg_color
        )
        self.text_area.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.text_area.yview)

        self.status_bar = tk.Label(
            self.root,
            text="Готово",
            bg=self.button_bg,
            fg=self.button_fg,
            anchor=tk.W
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def new_file(self):
        """Создает новый файл."""
        self.current_file = None
        self.text_area.delete(1.0, tk.END)
        self.root.title("Простой блокнот")
        self.status_bar.config(text="Создан новый файл")

    def open_file(self):
        """Открывает файл."""
        filename = filedialog.askopenfilename(
            title="Открыть файл",
            filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")]
        )

        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    content = f.read()

                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(1.0, content)

                self.current_file = filename
                self.root.title(f"Простой блокнот - {os.path.basename(filename)}")
                self.status_bar.config(text=f"Открыт файл: {os.path.basename(filename)}")

            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось открыть файл:\n{str(e)}")

    def save_file(self):
        """Сохраняет файл."""
        if self.current_file:
            self.save_to_file(self.current_file)
        else:
            self.save_as_file()

    def save_as_file(self):
        """Сохраняет файл с выбором имени."""
        filename = filedialog.asksaveasfilename(
            title="Сохранить файл как",
            defaultextension=".txt",
            filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")]
        )

        if filename:
            self.save_to_file(filename)
            self.current_file = filename
            self.root.title(f"Простой блокнот - {os.path.basename(filename)}")

    def save_to_file(self, filename):
        """Сохраняет текст в файл."""
        try:
            content = self.text_area.get(1.0, tk.END)

            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)

            self.status_bar.config(text=f"Файл сохранен: {os.path.basename(filename)}")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить файл:\n{str(e)}")

    def clear_text(self):
        """Очищает текстовое поле."""
        if messagebox.askyesno("Очистка", "Очистить текстовое поле?"):
            self.text_area.delete(1.0, tk.END)
            self.status_bar.config(text="Текст очищен")

    def show_about(self):
        """Показывает информацию о программе."""
        messagebox.showinfo(
            "О программе",
            "Простой блокнот\n\n"
            "Создан для демонстрации Tkinter\n"
            "Функции:\n"
            "- Создание и редактирование текста\n"
            "- Сохранение и открытие файлов\n"
            "- Очистка текста"
        )

    def run(self):
        """Запускает приложение."""
        self.root.mainloop()


def main():
    """Основная функция."""
    app = Notepad()
    app.run()


if __name__ == "__main__":
    main()