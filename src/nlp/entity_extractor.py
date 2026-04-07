import re
from datetime import datetime, timedelta


class EntityExtractor:
    def __init__(self):
        self.months = {
            "january", "february", "march", "april",
            "may", "june", "july", "august",
            "september", "october", "november", "december"
        }

    def extract(self, text: str) -> dict:
        """
        extract useful entities from the text
        """
        text = text.lower()
        entities = {}

        # percentages
        percentage = self._extract_percentage(text)
        if percentage is not None:
            entities["percentage"] = percentage

        # cource codes
        courses = self._extract_courses(text)
        if courses:
            entities["course_codes"] = courses

        dates = []

        # full dates
        explicit_dates = self._extract_dates(text)
        if explicit_dates:
            dates.extend(explicit_dates)

        # relative dates
        relative_dates = self._extract_relative_dates(text)
        if relative_dates:
            dates.extend(relative_dates)

        if dates:
            entities["dates"] = dates

        # fallback days
        days_data = self._extract_days(text, percentage)
        if days_data:
            dates.extend(days_data["dates"])

        if not explicit_dates:
            days_data = self._extract_days(text, percentage)
            if days_data:
                dates.extend(days_data["dates"])

        # remove duplicates
        if dates:
            dates = list(dict.fromkeys(dates))
            entities["dates"] = dates

        # months
        month = self._extract_month(text)
        if month:
            entities["month"] = month
        
        return entities

    def _extract_percentage(self, text: str):
        # find percentage like 75%
        match = re.search(r'(\d+)%', text)
        if match:
            return int(match.group(1))
        return None

    def _extract_dates(self, text: str):
        date_matches = re.findall(
            r'\b(\d{1,2})(?:st|nd|rd|th)?\s+(january|february|march|april|may|june|july|august|september|october|november|december)\b',
            text
        )

        if not date_matches:
            return None

        return [(int(day), month) for day, month in date_matches]

    def _extract_days(self, text: str, percentage: int | None):
        today = datetime.now()

        # extract ordinal days like 25th
        day_matches = re.findall(r'\b(\d{1,2})(?:st|nd|rd|th)\b', text)
        days = [int(d) for d in day_matches]

        # fallback numbers
        if not days:
            numbers = [
                        int(n) for n in re.findall(r'\b\d{1,2}\b', text)
                        if not re.search(rf"{n}\s+(january|february|march|april|may|june|july|august|september|october|november|december)", text)
                    ]

            if percentage is not None:
                numbers = [n for n in numbers if n != percentage]

            days = [n for n in numbers if n <= 31]

        if not days:
            return None

        # check if month exists in text
        month = self._extract_month(text)

        if not month:
            month = today.strftime("%B").lower()

        dates = [(day, month) for day in days]

        return {"dates": dates}

    def _extract_month(self, text: str):
        # find first month mentioned
        for month in self.months:
            if month in text:
                return month
        return None
    
    def _extract_courses(self, text: str):
        # find course codes like cse2005
        matches = re.findall(r'\b[a-z]{2,4}\s?\d{3,5}\b', text)
        if not matches:
            return None
        return [m.replace(" ", "").lower() for m in matches]
    

    def _extract_relative_dates(self, text: str):
        today = datetime.now()

        mapping = {
            "day before yesterday": -2,
            "yesterday": -1,
            "today": 0,
            "tomorrow": 1,
            "day after tomorrow": 2
        }

        results = []

        for phrase, offset in mapping.items():
            if re.search(rf"\b{phrase}\b", text):
                target_date = today + timedelta(days=offset)
                results.append((target_date.day, target_date.strftime("%B").lower()))

        return results if results else None