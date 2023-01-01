import json
import requests
from icalendar import Calendar, Event
from datetime import datetime


def GetContestList(url: str = "https://algcontest.rainng.com/") -> list:
    r = requests.get(url)
    if r.status_code == 200:
        return json.loads(r.text)
    return []


def GenerateICS(
        contestList: list, path: str = "./ICSVersion/Contests.ics", oldCal: Calendar = None
) -> str:
    cal = oldCal
    uid2event = {}
    if cal:
        for component in cal.walk():
            if component.name == "VEVENT":
                uid2event[component.get('uid')] = component
    else:
        cal = Calendar()
        cal.add('VERSION', '2.0')
        cal.add('PRODID', '各大OJ比赛日历ICS')
        cal.add('CALSCALE', 'GREGORIAN')
        cal.add('X-WR-CALNAME', '各大OJ比赛日历ICS')
        cal.add('X-APPLE-CALENDAR-COLOR', '#540EB9')
        cal.add('X-WR-TIMEZONE', 'Asia/Shanghai')

    for contest in contestList:
        curUid = contest['name'] + str(contest['startTimeStamp'])
        event = Event()
        if curUid in uid2event.keys():
            event = uid2event[curUid]
            event.add('uid', curUid)
            event.add('summary', contest['name'])
            event.add('dtstart', datetime.fromtimestamp(contest['startTimeStamp']))
            event.add('dtend', datetime.fromtimestamp(contest['endTimeStamp']))
            event.add('dtstamp', datetime.utcnow())
            event.add(
                'description',
                contest['link'] + " \n数据来源http://algcontest.rainng.com/",
                encode=False,
            )
        else:
            event.add('uid', curUid)
            event.add('summary', contest['name'])
            event.add('dtstart', datetime.fromtimestamp(contest['startTimeStamp']))
            event.add('dtend', datetime.fromtimestamp(contest['endTimeStamp']))
            event.add('dtstamp', datetime.utcnow())
            event.add(
                'description',
                contest['link'] + " \n数据来源http://algcontest.rainng.com/",
                encode=False,
            )
            cal.add_component(event)
        # print(event.to_ical())

    f = open(path, 'wb')
    f.write(cal.to_ical())
    f.close()


def main():
    data = GetContestList()
    try:
        ics = open("./ICSVersion/Contests.ics")
        cal = Calendar.from_ical(ics.read())
    except FileNotFoundError:
        cal = None
    GenerateICS(data, oldCal=cal)


if __name__ == "__main__":
    main()
