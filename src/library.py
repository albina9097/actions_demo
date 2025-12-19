class Book:
    def __init__(self, title, author, year):
        self.__title = title
        self.__author = author
        self.__year = year
        self.__available = True

    def get_title(self):
        return self.__title

    def get_author(self):
        return self.__author

    def get_year(self):
        return self.__year

    def is_available(self):
        return self.__available

    def mark_as_taken(self):
        self.__available = False

    def mark_as_returned(self):
        self.__available = True

    def __str__(self):
        status = 'доступна' if self.__available else 'недоступна'
        return f"{self.__title} ({self.__author}, {self.__year}) --- {status}"


class PrintedBook(Book):
    def __init__(self, title, author, year, pages, condition):
        super().__init__(title, author, year)
        self.pages = pages
        self.condition = condition

    def repair(self):
        if self.condition == "плохая":
            self.condition = "хорошая"
        elif self.condition == "хорошая":
            self.condition = "новая"

    def __str__(self):
        base_str = super().__str__()
        return f"{base_str}, {self.pages} стр., состояние: {self.condition}"


class EBook(Book):
    def __init__(self, title, author, year, file_size, format_):
        super().__init__(title, author, year)
        self.file_size = file_size
        self.format = format_

    def download(self):
        print(f"Книга '{self.get_title()}' загружается...")

    def __str__(self):
        base_str = super().__str__()
        return f"{base_str}, файл: {self.file_size} МБ, формат: {self.format}"


class User:
    def __init__(self, name):
        self.name = name
        self.__borrowed_books = []

    def borrow(self, book):
        if len(self.__borrowed_books) >= 3:
            print(f"{self.name} уже взял максимальное число книг!")
            return
        if book.is_available():
            book.mark_as_taken()
            self.__borrowed_books.append(book)
            print(f"{self.name} взял книгу '{book.get_title()}'")
        else:
            print("Книга недоступна")

    def return_book(self, book):
        if book in self.__borrowed_books:
            self.__borrowed_books.remove(book)
            book.mark_as_returned()
            print(f"{self.name} вернул книгу '{book.get_title()}'")
        else:
            print("Этой книги нет у пользователя")

    def show_books(self):
        if not self.__borrowed_books:
            print(f"У {self.name} нет книг")
        else:
            print(f"Книги пользователя {self.name}:")
            for b in self.__borrowed_books:
                print(" ---", b.get_title())

    def get_borrowed_books(self):
        return tuple(self.__borrowed_books)  # read-only


class Librarian(User):
    def add_book(self, library, book):
        library.add_book(book)

    def remove_book(self, library, title):
        library.remove_book(title)

    def register_user(self, library, user):
        library.add_user(user)


class Library:
    def __init__(self):
        self.__books = []
        self.__users = []

    def add_book(self, book):
        self.__books.append(book)

    def remove_book(self, title):
        for book in self.__books:
            if book.get_title() == title:
                self.__books.remove(book)
                return
        print("Книга не найдена")

    def add_user(self, user):
        self.__users.append(user)

    def find_book(self, title):
        for book in self.__books:
            if book.get_title() == title:
                return book
        return None

    def show_all_books(self):
        for book in self.__books:
            print(book)

    def show_available_books(self):
        for book in self.__books:
            if book.is_available():
                print(book)

    def lend_book(self, title, user_name):
        book = self.find_book(title)
        user = self.find_user(user_name)
        if not book:
            print("Книга не найдена")
            return
        if not user:
            print("Пользователь не найден")
            return
        user.borrow(book)

    def return_book(self, title, user_name):
        book = self.find_book(title)
        user = self.find_user(user_name)
        if book and user:
            user.return_book(book)
        else:
            print("Ошибка возврата")

    def find_user(self, name):
        for u in self.__users:
            if u.name == name:
                return u
        return None


if __name__ == '__main__':
    lib = Library()
    b1 = PrintedBook("Война и мир", "Толстой", 1869, 1225, "хорошая")
    b2 = EBook("Мастер и Маргарита", "Булгаков", 1966, 5, "epub")
    
    b3 = PrintedBook(
        "Преступление и наказание", 
        "Достоевский", 
        1866, 
        480, 
        "плохая"
    )
    
    user1 = User("Анна")
    librarian = Librarian("Мария")
    
    librarian.add_book(lib, b1)
    librarian.add_book(lib, b2)
    librarian.add_book(lib, b3)
    librarian.register_user(lib, user1)
    
    lib.lend_book("Война и мир", "Анна")
    user1.show_books()
    lib.return_book("Война и мир", "Fyf")
    b2.download()
    b3.repair()
    print(b3)