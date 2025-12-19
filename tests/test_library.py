import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
import pytest
from library import (
    Book,
    PrintedBook,
    EBook,
    User,
    Librarian,
    Library,
)


def test_book_creation():
    book = Book("Тест", "Автор", 2020)

    assert book.get_title() == "Тест"
    assert book.get_author() == "Автор"
    assert book.get_year() == 2020
    assert book.is_available() is True


def test_book_take_and_return():
    book = Book("Тест", "Автор", 2020)

    book.mark_as_taken()
    assert book.is_available() is False

    book.mark_as_returned()
    assert book.is_available() is True


def test_printed_book_repair():
    book = PrintedBook("Книга", "Автор", 2000, 300, "плохая")

    book.repair()
    assert book.condition == "хорошая"

    book.repair()
    assert book.condition == "новая"


def test_ebook_creation():
    ebook = EBook("Электронная", "Автор", 2021, 5, "pdf")

    assert ebook.file_size == 5
    assert ebook.format == "pdf"


def test_user_borrow_and_return():
    user = User("Анна")
    book = Book("Книга", "Автор", 2020)

    user.borrow(book)

    assert book.is_available() is False
    assert book in user.get_borrowed_books()

    user.return_book(book)

    assert book.is_available() is True
    assert book not in user.get_borrowed_books()


def test_user_cannot_borrow_more_than_three_books():
    user = User("Анна")
    books = [
        Book("К1", "А", 1),
        Book("К2", "А", 2),
        Book("К3", "А", 3),
        Book("К4", "А", 4),
    ]

    for b in books[:3]:
        user.borrow(b)

    user.borrow(books[3])

    assert len(user.get_borrowed_books()) == 3
    assert books[3].is_available() is True


def test_library_add_and_find_book():
    library = Library()
    book = Book("Тест", "Автор", 2020)

    library.add_book(book)

    found = library.find_book("Тест")
    assert found == book


def test_library_remove_book():
    library = Library()
    book = Book("Тест", "Автор", 2020)

    library.add_book(book)
    library.remove_book("Тест")

    assert library.find_book("Тест") is None


def test_library_lend_book():
    library = Library()
    user = User("Анна")
    book = Book("Тест", "Автор", 2020)

    library.add_book(book)
    library.add_user(user)

    library.lend_book("Тест", "Анна")

    assert book.is_available() is False
    assert book in user.get_borrowed_books()


def test_librarian_add_book_and_user():
    library = Library()
    librarian = Librarian("Мария")
    user = User("Анна")
    book = Book("Тест", "Автор", 2020)

    librarian.add_book(library, book)
    librarian.register_user(library, user)

    assert library.find_book("Тест") == book
    assert library.find_user("Анна") == user