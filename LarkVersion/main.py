from email import header
import json
import requests
import argparse
import os
import logging
import requests
from api import CanlanderApiClient
from flask import Flask, jsonify
from dotenv import load_dotenv, find_dotenv

# load env parameters form file named .env
load_dotenv(find_dotenv())

# load from env
APP_ID = os.getenv("APP_ID")
APP_SECRET = os.getenv("APP_SECRET")
VERIFICATION_TOKEN = os.getenv("VERIFICATION_TOKEN")
ENCRYPT_KEY = os.getenv("ENCRYPT_KEY")
LARK_HOST = os.getenv("LARK_HOST")
USER_ACCESS_TOKEN = os.getenv("USER_ACCESS_TOKEN")
from api import CanlanderApiClient


def GetContestList(url: str = "https://algcontest.rainng.com/") -> list:
    r = requests.get(url)
    if r.status_code == 200:
        return json.loads(r.text)
    return []

# def LinktoLark(ContestList: list, Client: CanlanderApiClient):
    
#     url = "https://open.feishu.cn/open-apis/calendar/v4/calendars?page_size=500"
#     payload = ''
#     headers = {
#         'Authorization': user_access_token
#     }
#     response = requests.request("GET", url, headers=headers, data=payload)
#     CalenderList = json.loads(response.text)["data"]["calendar_list"]
#     TargetCalanderId = ''
#     for Canlender in CalenderList:
#         if (Canlender["description"] == "OjContestCanlender"):
#             TargetCalanderId = Canlender["calendar_id"]
#     if TargetCalanderId == '':
#         url = "https://open.feishu.cn/open-apis/calendar/v4/calendars"
#         payload = json.dumps({
#             "color": 3,
#             "description": "OjContestCanlender",
#             "permissions": "private",
#             "summary": "OjContestCanlender",
#             "summary_alias": "OjContestCanlender"
#         })
#         headers = {
#             'Content-Type': 'application/json',
#             'Authorization': user_access_token
#         }
#         response = json.loads(requests.request(
#             "POST", url, headers=headers, data=payload).text)
#         TargetCalanderId = response['data']['calender']['calendar_id']
#     print(ContestList)
#     for Contest in ContestList:
#         url = "https://open.feishu.cn/open-apis/calendar/v4/calendars/"+ TargetCalanderId + "/events"
#         payload = json.dumps({
#             "attendee_ability": "can_see_others",
#             "color": -1,
#             "description": Contest["oj"] + ": " + Contest["name"] + "\n" + Contest["link"],
#             "end_time": {
#                 "timestamp": str(Contest["endTimeStamp"]),
#                 "timezone": "Asia/Shanghai"
#             },
#             "free_busy_status": "busy",
#             "need_notification": False,
#             "reminders": [
#                 {
#                     "minutes": 60
#                 }
#             ],
#             "start_time": {
#                 "timestamp": str(Contest["startTimeStamp"]),
#                 "timezone": "Asia/Shanghai"
#             },
#             "summary": Contest["oj"] + ": " + Contest["name"],
#             "visibility": "default"
#         })
#         headers = {
#             'Authorization': user_access_token,
#             'Content-Type': 'application/json'
#         }
#         response = requests.request("POST", url, headers=headers, data=payload)
#         print(response.text)

client = CanlanderApiClient(APP_ID, APP_SECRET, LARK_HOST)

def SubscribeCalander():
    url = "https://open.feishu.cn/open-apis/calendar/v4/calendars/:calendar_id/subscribe"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + USER_ACCESS_TOKEN,
    }
    payload = {
        "calendar_id": "feishu.cn_m6HKXwgZyLDes8qHUZAHad@group.calendar.feishu.cn",
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response)

if "__main__" == __name__:
    client.update(GetContestList())
    SubscribeCalander()
