import pytest
from src.nlp.entity_extractor import EntityExtractor


@pytest.fixture
def extractor():
    return EntityExtractor()


# -------------------- BASIC TESTS --------------------

def test_extract_percentage(extractor):
    text = "attendance over 75%"
    result = extractor.extract(text)

    assert result["percentage"] == 75


def test_extract_single_course(extractor):
    text = "for cse2005"
    result = extractor.extract(text)

    assert result["course_codes"] == ["cse2005"]


def test_extract_multiple_courses(extractor):
    text = "for cse2005 and ece1001"
    result = extractor.extract(text)

    assert set(result["course_codes"]) == {"cse2005", "ece1001"}


def test_extract_course_with_space(extractor):
    text = "for cse 2005"
    result = extractor.extract(text)

    assert result["course_codes"] == ["cse2005"]


# -------------------- DATE TESTS --------------------

def test_extract_dates_range(extractor):
    text = "between 25 march and 10 april"
    result = extractor.extract(text)

    assert result["dates"] == [(25, "march"), (10, "april")]


def test_full_query(extractor):
    text = "how many classes can i skip between 25 march and 10 april for cse2005 with 75%"
    result = extractor.extract(text)

    assert result["percentage"] == 75
    assert result["course_codes"] == ["cse2005"]
    assert (25, "march") in result["dates"]
    assert (10, "april") in result["dates"]


# -------------------- FALLBACK DAYS --------------------

def test_extract_days_only(extractor):
    text = "skip classes on 25th and 30th"
    result = extractor.extract(text)

    days = [d for d, _ in result["dates"]]
    assert set(days) == {25, 30}


def test_extract_days_from_numbers(extractor):
    text = "between 5 and 10"
    result = extractor.extract(text)

    days = [d for d, _ in result["dates"]]
    assert set(days) == {5, 10}


def test_percentage_not_in_days(extractor):
    text = "75% attendance and 25 classes"
    result = extractor.extract(text)

    assert result["percentage"] == 75

    days = [d for d, _ in result.get("dates", [])]
    assert 75 not in days


# -------------------- ADVANCED DATE CASES --------------------

def test_relative_and_ordinal_dates(extractor):
    text = "schedule for tomorrow and on 15th"
    result = extractor.extract(text)

    days = [d for d, _ in result["dates"]]
    assert len(days) == 2
    assert 15 in days


def test_relative_and_explicit_dates(extractor):
    text = "classes on tomorrow and 10 april"
    result = extractor.extract(text)

    assert any(day == 10 and month == "april" for day, month in result["dates"])
    assert len(result["dates"]) >= 2


def test_only_relative_dates(extractor):
    text = "classes for today and tomorrow"
    result = extractor.extract(text)

    assert len(result["dates"]) == 2


def test_multiple_relative_dates(extractor):
    text = "yesterday, today and tomorrow"
    result = extractor.extract(text)

    assert len(result["dates"]) == 3


def test_explicit_and_ordinal_mix(extractor):
    text = "between 10 april and 15th"
    result = extractor.extract(text)

    days = [d for d, _ in result["dates"]]
    assert 10 in days
    assert 15 in days


def test_no_duplicate_dates(extractor):
    text = "tomorrow and tomorrow"
    result = extractor.extract(text)

    assert len(result["dates"]) == 1


def test_ordinal_with_month_context(extractor):
    text = "on 15th april"
    result = extractor.extract(text)

    assert result["dates"] == [(15, "april")]


def test_numbers_and_percentage_mix(extractor):
    text = "75% attendance between 10 and 20"
    result = extractor.extract(text)

    days = [d for d, _ in result["dates"]]
    assert 10 in days and 20 in days
    assert 75 not in days


# -------------------- EDGE CASES --------------------

def test_no_entities(extractor):
    text = "hello how are you"
    result = extractor.extract(text)

    assert result == {}


def test_complex_query(extractor):
    text = "schedule for cse1008 tomorrow and 15th april"
    result = extractor.extract(text)

    assert "cse1008" in result["course_codes"]
    assert len(result["dates"]) >= 2