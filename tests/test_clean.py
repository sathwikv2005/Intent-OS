from src.preprocessing.clean import clean_text

def test_lowercase():
    assert clean_text("HELLO") == "hello"

def test_remove_punctuation():
    assert clean_text("hello!!!") == "hello"

def test_remove_extra_spaces():
    assert clean_text("hello    world") == "hello world"

def test_strip_edges():
    assert clean_text("   hello world   ") == "hello world"

def test_combined():
    text = "   Hello!!!   World   "
    assert clean_text(text) == "hello world"