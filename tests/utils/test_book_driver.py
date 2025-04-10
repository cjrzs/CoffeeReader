from src.utils.book_driver import get_book, list_books


def test_get_book():
    result = get_book("在咖啡变冷之前")
    return not result


def test_list_books():
    result = list_books()
    return not result


