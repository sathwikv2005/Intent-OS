from core.vtopClient import vtopClient
import datetime

client = vtopClient()

def login():
    res = client.checkLogin()
    if res.get("error"):
        return {"success": False, "error": res["error"]}

    return {"success": True}


def get_timetable(entities=None):
    res = client.getTimeTable()

    if res.get("error"):
        return {"success": False, "error": res["error"]}

    formatted = format_timetable(res["timetable"], entities)

    return {
        "success": True,
        "data": formatted
    }


def get_attendance(entities=None):
    res = client.getAttendance()

    if res.get("error"):
        return {"success": False, "error": res["error"]}

    formatted = format_attendance(res["attendance"], entities)

    return {
        "success": True,
        "data": formatted
    }

# def get_marks(entities):
#     return requests.get(f"{BASE_URL}/marks").json()


# def get_next_class(entities):
#     return requests.get(f"{BASE_URL}/next-class").json()


def calc_buffer_classes(min_percent, attended, total):
    p = int(min_percent)
    a = int(attended)
    t = int(total)

    percentage = (a * 100) / t

    if percentage < p:
        return {"type": "need", "classes": classes_needed(a, t, p)}
    else:
        return {"type": "skip", "classes": classes_can_skip(a, t, p)}


def classes_needed(a, t, p):
    current_percentage = (a / t) * 100
    if current_percentage >= p:
        return 0

    x = (p * t - 100 * a) / (100 - p)
    return int(x) + (1 if x % 1 > 0 else 0)  # ceil


def classes_can_skip(a, t, p):
    x = (a * 100) / p - t
    return max(int(x), 0)  # floor

def format_attendance(attendance_list, entities=None, min_percent=75):
    rows = []

    # Normalize filter list
    filter_codes = None
    if entities and entities.get("course_codes"):
        filter_codes = set(code.lower() for code in entities["course_codes"])

    for item in attendance_list:
        # Split courseDetails
        parts = item["courseDetails"].split(" - ")

        course_code = parts[0].lower()
        course_title = parts[1] if len(parts) > 1 else ""
        class_type = parts[len(parts)-1] if len(parts) > 2 else ""

        # Apply filter
        if filter_codes and course_code not in filter_codes:
            continue

        attended = int(item["attended"])
        total = int(item["totalClasses"])
        percent = int(item["percentage"])

        buffer = calc_buffer_classes(min_percent, attended, total)

        if buffer["type"] == "skip":
            buffer_str = f"Can Skip {buffer['classes']}"
        else:
            buffer_str = f"Must Attend {buffer['classes']}"

        rows.append([
            course_code.upper(),
            course_title,
            class_type,
            f"{attended}/{total}",
            f"{percent}%",
            buffer_str
        ])

    if not rows:
        return "No matching courses found."

    # Table formatting
    headers = ["Code", "Title", "Type", "Classes", "%", "Buffer"]

    col_widths = [max(len(str(row[i])) for row in rows + [headers]) for i in range(len(headers))]

    def format_row(row):
        return " | ".join(str(row[i]).ljust(col_widths[i]) for i in range(len(row)))

    table = []
    table.append(format_row(headers))
    table.append("-+-".join("-" * w for w in col_widths))

    for row in rows:
        table.append(format_row(row))

    return "\n".join(table)



def get_days_from_entities(entities):
    if not entities:
        return None

    days = set()

    # Case 1: explicit dates
    if entities.get("dates"):
        for d, m in entities["dates"]:
            try:
                date_obj = datetime.datetime.strptime(f"{d} {m} 2026", "%d %B %Y")
                days.add(date_obj.strftime("%a").upper()[:3])  # MON, TUE...
            except:
                continue

    return days if days else None


def format_timetable(timetable_data, entities=None):
    rows = []

    # Filters
    filter_days = get_days_from_entities(entities)

    filter_courses = None
    if entities and entities.get("course_codes"):
        filter_courses = set(code.lower() for code in entities["course_codes"])

    for day_data in timetable_data:
        day = day_data["day"]

        # Filter by day
        if filter_days and day not in filter_days:
            continue

        for cls in day_data["classes"]:
            course_code = cls["courseCode"]
            course = course = f"{course_code} - {cls.get('courseTitle', '')}"
            
            if len(course) > 40:
                course = course[:37] + "..."

            # Filter by course
            if filter_courses and course_code.lower() not in filter_courses:
                continue

            start = cls["timings"]["start"]
            end = cls["timings"]["end"]

            rows.append([
                day,
                f"{start}-{end}",
                course,
                cls["type"],
                cls["slot"],
                cls["venue"]
            ])

    if not rows:
        return "No matching timetable entries found."

    # Sort by day + time
    day_order = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
    rows.sort(key=lambda x: (day_order.index(x[0]), x[1]))

    # Table formatting
    headers = ["Day", "Time", "Course", "Type", "Slot", "Venue"]

    col_widths = [max(len(str(row[i])) for row in rows + [headers]) for i in range(len(headers))]

    def format_row(row):
        return " | ".join(str(row[i]).ljust(col_widths[i]) for i in range(len(row)))

    table = []
    table.append(format_row(headers))
    table.append("-+-".join("-" * w for w in col_widths))

    for row in rows:
        table.append(format_row(row))

    return "\n".join(table)