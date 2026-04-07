import re

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


        # dates
        dates_data = self._extract_dates(text)
        if dates_data:
            entities.update(dates_data)
            return entities  # stop early if full dates exist

        # fallback days
        days_data = self._extract_days(text, percentage)
        if days_data:
            entities.update(days_data)

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
        # find full dates like 25 march
        date_matches = re.findall(
            r'\b(\d{1,2})(?:st|nd|rd|th)?\s+(january|february|march|april|may|june|july|august|september|october|november|december)\b',
            text
        )

        if not date_matches:
            return None

        dates = [(int(day), month) for day, month in date_matches]

        data = {
            "dates": dates
        }

        if len(dates) >= 2:
            data["start_date"] = f"{dates[0][0]} {dates[0][1]}"
            data["end_date"] = f"{dates[1][0]} {dates[1][1]}"

        return data

    def _extract_days(self, text: str, percentage: int | None):
        # extract ordinal days like 25th
        day_matches = re.findall(r'\b(\d{1,2})(?:st|nd|rd|th)\b', text)
        days = [int(d) for d in day_matches]

        # fallback numbers
        if not days:
            numbers = [int(n) for n in re.findall(r'\b\d{1,2}\b', text)]

            if percentage is not None:
                numbers = [n for n in numbers if n != percentage]

            days = [n for n in numbers if n <= 31]

        if days:
            return {"days": days}

        return None

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
        