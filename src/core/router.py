from core.actions import get_timetable, get_attendance

ROUTES = {
    "get_timetable": get_timetable,
    "get_attendance": get_attendance,
}

def route(intent, entities=None):
    if intent not in ROUTES:
        return {"error": "Unknown intent"}

    try:
        func = ROUTES[intent]

        # if function needs entities later
        res = func(entities)
        if res.get("data"):
            return res["data"]
        return res


    except Exception as e:
        return {"error": str(e)}