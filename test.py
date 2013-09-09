from library import Book, Library, LibraryTerminalInterface
import pytest
import copy

@pytest.fixture
def book():
    return Book("The Grapes of Wrath", "John Steinbeck")

@pytest.fixture
def grapes(book):
    return book

@pytest.fixture
def mice():
    return Book("Of Mice and Men", "John Steinbeck")

@pytest.fixture
def moby():
    return Book("Moby Dick", "Herman Melville")

@pytest.fixture
def library():
    return Library()

@pytest.fixture
def filled_library(library, grapes, mice, moby):
    for book in [grapes, mice, moby]:
        library.add(book.title, book.author)
    return library

def test_create_book(book):
    assert book

def test_book_str(book):
    expected = '"The Grapes of Wrath" by John Steinbeck (unread)'
    result = str(book)
    assert expected == result

def test_library(library):
    assert library

def test_add_book_to_library(library, book):
    library.add(book.title, book.author)
    book_in_lib = library.books[0]
    assert book_in_lib.title == book.title
    assert book_in_lib.author == book.author
    assert book_in_lib.read is not True

def test_book_equality(library, book):
    some_other_book = Book("other_title", "other_author")
    library.add(book.title, book.author)
    book_in_lib = library.books[0]
    assert book_in_lib == book
    assert not (book_in_lib == some_other_book)

def test_add_instance(library, book):
    library.add_instance(book)
    assert book in library.books

def test_show_all(filled_library, grapes, mice, moby):
    shown = filled_library.show('all')
    for book in [grapes, mice, moby]:
        assert book in shown

def test_show_unread_contains_all_unread(filled_library, grapes, mice, moby):
    filled_library.read(grapes.title)
    shown = filled_library.show('unread')
    for book in [mice, moby]:
        assert book in shown

def test_show_unread_does_not_contain_read(filled_library, grapes, mice, moby):
    reading_list = [grapes, mice]
    for book in reading_list:
        filled_library.read(book.title)
    shown = filled_library.show('unread')
    for book in reading_list:
        assert not (book in shown)

def test_show_all_by_author(filled_library, grapes, mice, moby):
    steinbooks = [grapes, mice]
    shown = filled_library.show('all', grapes.author)
    for book in steinbooks:
        assert book in shown
    assert not (moby in shown)

@pytest.fixture
def ui():
    return LibraryTerminalInterface()

def test_ui_query_add(ui, book):
    result = ui.parse_query('add "{title}" "{author}"'.format(
        title=book.title,
        author=book.author))
    assert result == ('add', [book.title, book.author])

def test_ui_parse_add_good_input(ui, book):
    good_input = '"{title}" "{author}"'.format(
        title=book.title,
        author=book.author)
    result = ui.parse_add(good_input)
    assert result == [book.title, book.author]

def test_ui_parse_add_bad_input(ui):
    bad_inputs = [
        '"too" "many" "args wrapped in double quotes"',
        '"too few args wrapped in doubles"', #too few args
        'no args wrapped in doubles'
    ]
    for bad_input in bad_inputs:
        with pytest.raises(Exception):
            ui.parse_add(bad_input)

def test_ui_parse_read(ui, book):
    good_input = '"{title}"'.format(title = book.title)
    assert ui.parse_read(good_input) == [book.title]

def test_ui_parse_read_bad_input(ui):
    bad_inputs = [
        'title not wrapped in double quotes',
        '"title" with extra data outside of double quotes',
        '"too many" "things wrapped in doubles"'
    ]
    for bad_input in bad_inputs:
        with pytest.raises(Exception):
            ui.parse_read(bad_input)

def test_ui_parse_show_all(ui):
    good_input = 'all'
    assert ui.parse_show(good_input) == ['all']

def test_ui_parse_show_all_by_author(ui, book):
    good_input = 'all by "{author}"'.format(author=book.author)
    assert ui.parse_show(good_input) == ['all', book.author]

def test_ui_parse_show_unread(ui, book):
    good_input = 'unread'
    assert ui.parse_show(good_input) == ['unread']

def test_ui_parse_show_unread_by_author(ui, book):
    good_input = 'unread by "{author}"'.format(author=book.author)
    assert ui.parse_show(good_input) == ['unread', book.author]

def test_ui_parse_show_bad_input(ui):
    bad_input = 'bad_input'
    with pytest.raises(Exception):
        ui.parse_show(bad_input)

def test_ui_execute_add(ui, book):
    ui.execute('add', [book.title, book.author])
    assert book in ui.library.books

def test_ui_execute_read(ui, book):
    ui.library.add_instance(book)
    ui.execute('read', [book.title])
    assert ui.library.books[0].read

def test_ui_execute_show(ui, filled_library):
    ui.library = filled_library
    pass
