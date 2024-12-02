import pytest
# from app.exceptions.input_errors import EmptyTextError
from app.utils.split_text import TextSplitter

# Тесты для конструктора
def test_textsplitter_init_with_valid_text():
    splitter = TextSplitter("abcdefghijk")
    assert splitter.text == "abcdefghijk"

def test_textsplitter_init_with_invalid_type():
    with pytest.raises(TypeError, match="Входные данные должны быть строкой."):
        TextSplitter(123)

# Тесты для метода split
def test_split_even_division():
    splitter = TextSplitter("abcdefghij")  # 10 символов
    parts = splitter.split()
    assert parts == ("1. abcde", "2. fgh", "3. ij")

def test_split_with_remainder():
    splitter = TextSplitter("abcdefghi")  # 9 символов
    parts = splitter.split()
    assert parts == ("1. abc", "2. def", "3. ghi")

# def test_split_with_empty_string():
#     splitter = TextSplitter("")
#     with pytest.raises(EmptyTextError):
#         splitter.split()

# Тест для представления объекта
def test_repr():
    splitter = TextSplitter("abcdefghij")
    assert repr(splitter) == "TextSplitter(text='abcdefghi...')"

# Дополнительные тесты
def test_split_single_character():
    splitter = TextSplitter("a")
    parts = splitter.split()
    assert parts == ("1. a", "2. ", "3. ")

def test_split_two_characters():
    splitter = TextSplitter("ab")
    parts = splitter.split()
    assert parts == ("1. a", "2. b", "3. ")

def test_split_three_characters():
    splitter = TextSplitter("abc")
    parts = splitter.split()
    assert parts == ("1. a", "2. b", "3. c")
