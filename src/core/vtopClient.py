import requests

BASE_URL = "http://localhost:6700/api/"  # your Node API

class vtopClient:
    def __init__(self):
        self.csrf = None
        self.cookie = None
        self.sem = None
        self._timetable = None
        self._attendance = None
        self.login()

    def checkLogin(self):
        if self.csrf == None or self.cookie == None or self.sem == None:
            return self.login()
        res = self.getSem()
        if res.get("error"):
             return self.login()
        return {"success" : True}

    def getSem(self):
        res = requests.get(f"{BASE_URL}/semids")
        data = res.json()
        if(res.status_code != 200):
            return {"success" : False, "error": data.get("error", "Login failed")}
        
        self.sem = data["semesters"][0].semId
        return {"success" : True}

    def login(self, tries = 0):
        response = requests.post(f"{BASE_URL}/login/autocaptcha")
        
        if response.status_code == 500:
                return {"success" : False, "error": "VTOP server might be down"}

        data = response.json()
        if response.status_code == 401:
                error = data.get("error", "").lower()

                if ("csrf" in error or "captcha" in error) and tries < 5:
                    return self.login(tries + 1)

                return {"success" : False, "error": data.get("error", "Login failed")}

        self.csrf = data.csrf
        self.cookie = next((c["value"] for c in data.get("cookies", []) if c.get("key") == "JSESSIONID"),None)

        res = self.getSem()
        if res.get("error"):
             return {"success" : False, "error": res.get("error", "Login failed")}
        return {"success" : True}
      

    def getTimeTable(self):
        if self._timetable is not None:
            return {"success" : True, "timetable": self._timetable}
        res = requests.get(f"{BASE_URL}/timetable?jsessionId={self.cookie}&csrf={self.csrf}")
        data = res.json()
        if(res.status_code != 200):
              return {"success" : False, "error": data.get("error", "Timetable fetch failed")}
        
        timetable = data.get("timeTable", [])
        self._timetable = timetable
        return {"success" : True, "timetable": timetable}
    

    def getAttendance(self):
        if self._attendance is not None:
            return {"success" : True, "timetable": self._attendance}
        res = requests.get(f"{BASE_URL}/timetable?jsessionId={self.cookie}&csrf={self.csrf}&semID={self.sem}")
        data = res.json()
        if(res.status_code != 200):
              return {"success" : False, "error": data.get("error", "Attendance fetch failed")}
        
        attendance = data.get("attendance", [])
        self._attendance = attendance
        return {"success" : True, "attendance": attendance}