import pytest
from src.nlp.entity_extractor import EntityExtractor


@pytest.fixture
def extractor():
    return EntityExtractor()


# percentages

def test_extract_percentage(extractor):
    text = "attendance over 75%"
    result = extractor.extract(text)

    assert result["percentage"] == 75


# single course

def test_extract_single_course(extractor):
    text = "for cse2005"
    result = extractor.extract(text)

    assert result["course_codes"] == ["cse2005"]


# multiple courses

def test_extract_multiple_courses(extractor):
    text = "for cse2005 and ece1001"
    result = extractor.extract(text)

    assert set(result["course_codes"]) == {"cse2005", "ece1001"}


# course with space

def test_extract_course_with_space(extractor):
    text = "for cse 2005"
    result = extractor.extract(text)

    assert result["course_codes"] == ["cse2005"]


# full date range

def test_extract_dates_range(extractor):
    text = "between 25 march and 10 april"
    result = extractor.extract(text)

    assert result["start_date"] == "25 march"
    assert result["end_date"] == "10 april"
    assert result["dates"] == [(25, "march"), (10, "april")]


# full query (real case)

def test_full_query(extractor):
    text = "how many classes can i skip between 25 march and 10 april for cse2005 with 75%"
    result = extractor.extract(text)

    assert result["percentage"] == 75
    assert result["course_codes"] == ["cse2005"]
    assert result["start_date"] == "25 march"
    assert result["end_date"] == "10 april"


# fallback days (no month)

def test_extract_days_only(extractor):
    text = "skip classes on 25th and 30th"
    result = extractor.extract(text)

    assert result["days"] == [25, 30]


# fallback numbers without percentage

def test_extract_days_from_numbers(extractor):
    text = "between 5 and 10"
    result = extractor.extract(text)

    assert result["days"] == [5, 10]


# ensure percentage not mixed with days

def test_percentage_not_in_days(extractor):
    text = "75% attendance and 25 classes"
    result = extractor.extract(text)

    assert result["percentage"] == 75
    assert 75 not in result.get("days", [])