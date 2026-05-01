import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

DATA_FILE = "books.json"

class BookTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Tracker")
        self.books = []
        self.load_books()

        # --- Создание виджетов ---
        self.create_widgets()
        self.update_treeview()

    def create_widgets(self):
        # Поля ввода
        tk.Label(self.root, text="Название:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.title_entry = tk.Entry(self.root, width=30)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Автор:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.author_entry = tk.Entry(self.root, width=30)
        self.author_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Жанр:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.genre_entry = tk.Entry(self.root, width=30)
        self.genre_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Страниц:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.pages_entry = tk.Entry(self.root, width=30)
        self.pages_entry.grid(row=3, column=1, padx=5, pady=5)

        # Кнопка добавления
        tk.Button(self.root, text="Добавить книгу", command=self.add_book).grid(
            row=4, column=0, columnspan=2, pady=10)

        # Таблица (Treeview)
        self.tree = ttk.Treeview(self.root, columns=("author", "genre", "pages"), show="headings")
        self.tree.heading("author", text="Автор")
        self.tree.heading("genre", text="Жанр")
        self.tree.heading("pages", text="Страниц")
        self.tree.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        # Фильтры
        tk.Label(self.root, text="Фильтр по жанру:").grid(row=6, column=0, padx=5, sticky="e")
        self.filter_genre = tk.Entry(self.root)
        self.filter_genre.grid(row=6, column=1, padx=5, pady=2)

        tk.Label(self.root, text="Фильтр по страницам (>):").grid(row=7, column=0, padx=5, sticky="e")
        self.filter_pages = tk.Entry(self.root)
        self.filter_pages.grid(row=7, column=1, padx=5, pady=2)

        tk.Button(self.root, text="Применить фильтр", command=self.apply_filter).grid(
            row=8, column=0, columnspan=2, pady=5)

    def add_book(self):
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        genre = self.genre_entry.get().strip()
        pages_str = self.pages_entry.get().strip()

        # Валидация
        if not title or not author or not genre or not pages_str:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
            return

        if not pages_str.isdigit():
            messagebox.showerror("Ошибка", "Количество страниц должно быть числом!")
            return

        pages = int(pages_str)

        book = {"title": title, "author": author, "genre": genre, "pages": pages}
        self.books.append(book)
        self.save_books()
        self.update_treeview()

    def update_treeview(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        for book in self.books:
            self.tree.insert("", "end", values=(book["author"], book["genre"], book["pages"]))

    def apply_filter(self):
        genre_filter = self.filter_genre.get().strip().lower()
        try:
            pages_filter = int(self.filter_pages.get())
        except:
            pages_filter = 0

        filtered_books = [
            b for b in self.books
            if (not genre_filter or genre_filter in b["genre"].lower()) and b["pages"] > pages_filter
        ]

        for i in self.tree.get_children():
            self.tree.delete(i)

        for book in filtered_books:
            self.tree.insert("", "end", values=(book["author"], book["genre"], book["pages"]))

    def save_books(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.books, f, ensure_ascii=False, indent=4)

    def load_books(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                self.books = json.load(f)


if __name__ == "__main__":
    root = tk.Tk()
    app = BookTrackerApp(root)
    root.mainloop()
