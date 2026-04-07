from src.preprocessing.tokenize import tokenize

def test_basic_tokenization():
    assert tokenize("hello world") == ["hello", "world"]

def test_multiple_spaces():
    assert tokenize("hello    world") == ["hello", "world"]

def test_stopword_removal():
    assert tokenize("show my timetable") == ["show", "timetable"]
    
def test_stopword_removal():
    assert tokenize("show the timetable") == ["show", "timetable"]

def test_empty_input():
    assert tokenize("") == []