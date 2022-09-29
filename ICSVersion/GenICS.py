import json
import pytz
import requests
from icalendar import Calendar, Event
from datetime import datetime


def GetContestList(url: str = "https://algcontest.rainng.com/") -> list:
    r = requests.get(url)
    if r.status_code == 200:
        return json.loads(r.text)
    return []


def GenerateICS(contestList: list, path: str = "./sample.ics", oldCal: Calendar = None) -> str:
    cal = oldCal
    if cal == None:
        cal = Calendar()
    cal.add('VERSION', '2.0')
    cal.add('prodid', '各大OJ比赛日历ICS')
    cal.add('X-WR-CALNAME', '各大OJ比赛日历ICS')
    cal.add('X-APPLE-CALENDAR-COLOR', '#540EB9')
    cal.add('X-WR-TIMEZONE', 'Asia/Shanghai')
    for contest in contestList:
        event = Event()
        event.add('uid', contest['name'] + str(contest['startTimeStamp']))
        event.add('summary', contest['name'])
        dtstart = datetime.fromtimestamp(contest['startTimeStamp'])
        dtend = datetime.fromtimestamp(contest['endTimeStamp'])
        dstamp = datetime.utcnow()
        event.add('dtstart', dtstart)
        event.add('dtend', dtend)
        event.add('dtstamp', dstamp)
        event.add('description', contest['link'] + " \n数据来源http://algcontest.rainng.com/", encode=False)
        cal.add_component(event)
        # print(event.to_ical())

    f = open(path, 'wb')
    f.write(cal.to_ical())
    f.close()


if __name__ == "__main__":
    with open("../SampleData/AlgContest.json") as f:
        GenerateICS(json.loads(f.read()))
