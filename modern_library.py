import json
import os
from dataclasses import asdict, dataclass
from typing import List, Optional

DATA_FILE = "books.json"

@dataclass
class Book:
    title: str
    isbn: str
    status: str


def load_books() -> List[Book]:
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

    books: List[Book] = []
    for item in data:
        if isinstance(item, dict) and {"title", "isbn", "status"}.issubset(item.keys()):
            books.append(Book(title=item["title"], isbn=item["isbn"], status=item["status"]))
    return books


def save_books(books: List[Book]) -> None:
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([asdict(book) for book in books], f, ensure_ascii=False, indent=2)


def find_book_by_isbn(books: List[Book], isbn: str) -> Optional[Book]:
    isbn = isbn.strip()
    for book in books:
        if book.isbn == isbn:
            return book
    return None


def show_books(books: List[Book]) -> None:
    if not books:
        print("No books available")
        return

    for book in books:
        print(f"書名: {book.title}, ISBN: {book.isbn}, 狀態: {book.status}")


def add_book(books: List[Book], raw: str) -> None:
    parts = [part.strip() for part in raw.split("/")]
    if len(parts) != 3 or not all(parts):
        print("Format Error")
        return

    title, isbn, status = parts
    if find_book_by_isbn(books, isbn) is not None:
        print("ISBN Exist")
        return

    books.append(Book(title=title, isbn=isbn, status=status))
    print("Success")


def borrow_book(books: List[Book], isbn: str) -> None:
    book = find_book_by_isbn(books, isbn)
    if book is None:
        print("ISBN Not Found")
        return

    book.status = "borrowed"
    print("Updated")


def print_help() -> None:
    print("Commands:")
    print("  add <title>/<isbn>/<status>")
    print("  show")
    print("  borrow <isbn>")
    print("  exit")


def main() -> None:
    books = load_books()
    print("=== 圖書管理系統 v0.1 (Modern) ===")
    print_help()

    while True:
        try:
            op = input("> ").strip()
        except EOFError:
            break

        if op == "exit":
            save_books(books)
            print("系統關閉")
            break

        if op == "show":
            show_books(books)
            continue

        if op.startswith("add "):
            add_book(books, op[4:])
            continue

        if op.startswith("borrow "):
            borrow_book(books, op[7:])
            continue

        print("Unknown Command")


if __name__ == "__main__":
    main()
