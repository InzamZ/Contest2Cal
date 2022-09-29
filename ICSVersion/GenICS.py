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


def GenerateICS(contestList: list, path: str = "./ICSVersion/sample.ics", oldCal: Calendar = None) -> str:
    cal = oldCal
    uid2event = {}
    if cal:
        for component in cal.walk():
            if (component.name == "VEVENT"):
                uid2event[component.get('uid')] = component
    else:
        cal = Calendar()
        cal.add('VERSION', '2.0')
        cal.add('prodid', '各大OJ比赛日历ICS')
        cal.add('X-WR-CALNAME', '各大OJ比赛日历ICS')
        cal.add('X-APPLE-CALENDAR-COLOR', '#540EB9')
        cal.add('X-WR-TIMEZONE', 'Asia/Shanghai')

    for contest in contestList:
        curUid = contest['name'] + str(contest['startTimeStamp'])
        event = Event()
        if curUid in uid2event.keys():
            event = uid2event[curUid]
            event['uid'] = curUid
            event['summary'] = contest['name']
            event['dtstart'] = datetime.fromtimestamp(
                contest['startTimeStamp'])
            event['dtend'] = datetime.fromtimestamp(contest['endTimeStamp'])
            event['dtstamp'] = datetime.utcnow()
            event['dtstamp'] = contest['link'] + " \n数据来源http://algcontest.rainng.com/"
        else:
            event.add('uid', curUid)
            event.add('summary', contest['name'])
            event.add('dtstart', datetime.fromtimestamp(
                contest['startTimeStamp']))
            event.add('dtend', datetime.fromtimestamp(contest['endTimeStamp']))
            event.add('dtstamp', datetime.utcnow())
            event.add(
                'description', contest['link'] + " \n数据来源http://algcontest.rainng.com/", encode=False)
        cal.add_component(event)
        # print(event.to_ical())

    f = open(path, 'wb')
    f.write(cal.to_ical())
    f.close()


if __name__ == "__main__":
    data = open("./SampleData/AlgContest.json")
    cal = None
    try:
        ics = open("./ICSVersion/sample.ics")
        cal = Calendar.from_ical(ics.read())
    except:
        cal = None
        
    GenerateICS(json.loads(data.read()), oldCal=cal)
