from core.vtopClient import vtopClient

client = vtopClient()

def login():
    res = client.checkLogin()
    if res.get("error"):
        return {"success": False, "error": res["error"]}

    return {"success": True}


def get_timetable():
    res = client.getTimeTable()
    if res.get("error"):
        return {"success": False, "error": res["error"]}

    return {"success": True, "data": res["timetable"]}


def get_attendance():
    res = client.getAttendance()
    if res.get("error"):
        return {"success": False, "error": res["error"]}

    return {"success": True, "data": res["attendance"]}


# def get_marks(entities):
#     return requests.get(f"{BASE_URL}/marks").json()


# def get_next_class(entities):
#     return requests.get(f"{BASE_URL}/next-class").json()