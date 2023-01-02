import getopt
import json
import logging
import sys
import requests
from icalendar import Calendar, Event
from datetime import datetime


def GenerateICSFromAlg(
    path: str = "./ICSVersion/ContestsAlg.ics",
    oldCal: Calendar = None,
    tg_bot_token: str = None,
    tg_chat_id: str = None,
) -> str:
    contest_list = []
    new_contest = []
    r = requests.get("https://algcontest.rainng.com/")
    if r.status_code == 200:
        contest_list = json.loads(r.text)
    else:
        logging.error("Failed to get contest list from algcontest.rainng.com")
        sys.exit(2)
    cal = oldCal
    uid_hash = {}
    if cal:
        for component in cal.walk():
            if component.name == "VEVENT":
                uid_hash[component.get("uid")] = component
    else:
        cal = Calendar()
        cal.add("VERSION", "2.0")
        cal.add("PRODID", "各大OJ比赛日历ICS")
        cal.add("CALSCALE", "GREGORIAN")
        cal.add("X-WR-CALNAME", "各大OJ比赛日历ICS")
        cal.add("X-APPLE-CALENDAR-COLOR", "#540EB9")
        cal.add("X-WR-TIMEZONE", "Asia/Shanghai")

    for contest in contest_list:
        contest_uid = contest["name"] + str(contest["startTimeStamp"])
        event = Event()
        event.add("uid", contest_uid)
        event.add("summary", contest["name"])
        event.add("dtstart", datetime.fromtimestamp(contest["startTimeStamp"]))
        event.add("dtend", datetime.fromtimestamp(contest["endTimeStamp"]))
        event.add("dtstamp", datetime.utcnow())
        event.add(
            "description",
            contest["link"] + " \n数据来源http://algcontest.rainng.com/",
            encode=False,
        )
        if contest_uid in uid_hash.keys():
            uid_hash[contest_uid] = event
            new_contest.append(contest["name"])
        else:
            cal.add_component(event)

    if tg_bot_token and tg_chat_id:
        text = ""
        for contest in new_contest:
            text = text + contest + "%0a"
        if text != "":
            text = "新的比赛%0a" + text
            text = text.replace(" ", "%20")
            text = text.replace("&", "%26")
            text = text.replace("#", "%23")
            r = requests.get(
                f"https://api.telegram.org/bot{tg_bot_token}/sendMessage?chat_id={tg_chat_id}&text={text}"
            )

    f = open(path, "wb")
    f.write(cal.to_ical())
    f.close()


def GenerateICSFromSdutacm(
    oldCal: Calendar = None,
    tg_bot_token: str = None,
    tg_chat_id: str = None,
) -> str:
    contest_list = []
    new_contest = []
    path = "./ICSVersion/ContestsSdutacm.ics"
    r = requests.get("https://contests.sdutacm.cn/contests.json")
    if r.status_code == 200:
        contest_list = json.loads(r.text)
    else:
        logging.error("Failed to get contest list from contests.sdutacm.cn")
        sys.exit(2)
    cal = oldCal
    uid_hash = {}
    if cal:
        for component in cal.walk():
            if component.name == "VEVENT":
                uid_hash[component.get("uid")] = component
    else:
        cal = Calendar()
        cal.add("VERSION", "2.0")
        cal.add("PRODID", "各大OJ比赛日历ICS")
        cal.add("CALSCALE", "GREGORIAN")
        cal.add("X-WR-CALNAME", "各大OJ比赛日历ICS")
        cal.add("X-APPLE-CALENDAR-COLOR", "#540EB9")
        cal.add("X-WR-TIMEZONE", "Asia/Shanghai")

    """ contest
    {
        "source": "CodeChef",
        "name": "Past ZCO Problems",
        "link": "https://www.codechef.com/ZCOPRAC",
        "contest_id": "ZCOPRAC",
        "start_time": "2018-11-04T18:30:00+00:00",
        "end_time": "2024-04-26T18:30:00+00:00",
        "hash": "96d18304d8abc6b1a83314dc64d76507ac41ab61"
    }
    """
    for contest in contest_list:
        contest_uid = contest["hash"]
        contest_summary = f'{contest["source"]}: {contest["name"]}'
        contest_start_time = datetime.fromisoformat(contest["start_time"])
        contest_end_time = datetime.fromisoformat(contest["end_time"])
        contest_stamp = datetime.utcnow()
        contest_description = f'{contest["link"]} \n数据来源https://contests.sdutacm.cn/'
        event = Event()
        event.add("uid", contest_uid)
        event.add("summary", contest_summary)
        event.add("dtstart", contest_start_time)
        event.add("dtend", contest_end_time)
        event.add("dtstamp", contest_stamp)
        event.add("description", contest_description, encode=False)
        if contest_uid in uid_hash.keys():
            uid_hash[contest_uid] = event
        else:
            new_contest.append(contest_summary)
            cal.add_component(event)
            # print(event.to_ical())

    if tg_bot_token and tg_chat_id:
        text = ""
        for contest in new_contest:
            text = text + contest + "%0a"
        if text != "":
            text = "新的比赛%0a" + text
            text = text.replace(" ", "%20")
            text = text.replace("&", "%26")
            text = text.replace("#", "%23")
            r = requests.get(
                f"https://api.telegram.org/bot{tg_bot_token}/sendMessage?chat_id={tg_chat_id}&text={text}"
            )

    f = open(path, "wb")
    f.write(cal.to_ical())
    f.close()


def main(argv):
    info_source = "sdutacm"
    tg_bot_token = None
    tg_chat_id = None
    try:
        opts, args = getopt.getopt(
            argv, "s:", ["source=", "tg_bot_token=", "tg_chat_id="]
        )
    except getopt.GetoptError:
        print("GenICS.py -s <source>")
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-s", "--source"):
            info_source = arg
        elif opt in ("--tg_bot_token"):
            tg_bot_token = arg
        elif opt in ("--tg_chat_id"):
            tg_chat_id = arg
    if info_source == "sdutacm":
        try:
            ics = open("./ICSVersion/ContestsAlg.ics")
            cal = Calendar.from_ical(ics.read())
        except FileNotFoundError:
            cal = None
        GenerateICSFromSdutacm(
            oldCal=cal, tg_bot_token=tg_bot_token, tg_chat_id=tg_chat_id
        )
    else:
        try:
            ics = open("./ICSVersion/ContestsSdutacm.ics")
            cal = Calendar.from_ical(ics.read())
        except FileNotFoundError:
            cal = None
        GenerateICSFromAlg(oldCal=cal, tg_bot_token=tg_bot_token, tg_chat_id=tg_chat_id)


if __name__ == "__main__":
    main(sys.argv[1:])
