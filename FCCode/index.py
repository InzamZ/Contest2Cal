# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from doctest import master
import sys

from typing import List
import json
import requests
import os
import logging

# load from env
APP_ID = os.getenv("APP_ID")
APP_SECRET = os.getenv("APP_SECRET")
VERIFICATION_TOKEN = os.getenv("VERIFICATION_TOKEN")
ENCRYPT_KEY = os.getenv("ENCRYPT_KEY")
LARK_HOST = os.getenv("LARK_HOST")
USER_ACCESS_TOKEN = os.getenv("USER_ACCESS_TOKEN")
ENDPOINT = os.getenv("ENDPOINT")
ACCESSKEYID = os.getenv("ACCESSKEYID")
ACCESSKEYSECRET = os.getenv("ACCESSKEYSECRET")
MASTER_ID = os.getenv("MASTER_ID")
TGBOTTOKEN = os.getenv("TGBOTTOKEN")
TGBOTENABLE = os.getenv("TGBOTENABLE")

# const
TENANT_ACCESS_TOKEN_URI = "/open-apis/auth/v3/tenant_access_token/internal"
CanlanderURI = ""

# count
AddCnt = 0

class CanlanderApiClient(object):
    def __init__(self, app_id, app_secret, lark_host):
        self._app_id = app_id
        self._app_secret = app_secret
        self._lark_host = lark_host
        self._tenant_access_token = ""

    @property
    def tenant_access_token(self):
        return self._tenant_access_token

    def update(self, ContestList: list):
        # 更新获取新的应用鉴权口令
        self._authorize_tenant_access_token()

        url = "https://open.feishu.cn/open-apis/calendar/v4/calendars?page_size=500"
        payload = ""
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.tenant_access_token,
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        CanlanderApiClient._check_error_response(response)
        CalenderList = json.loads(response.text)["data"]["calendar_list"]
        TargetCalanderId = ""
        for Canlender in CalenderList:
            if Canlender["description"] == "OjContestCanlender":
                TargetCalanderId = Canlender["calendar_id"]
        if TargetCalanderId == "":
            url = "https://open.feishu.cn/open-apis/calendar/v4/calendars"
            payload = json.dumps(
                {
                    "color": -1,
                    "description": "OjContestCanlender",
                    "permissions": "public",
                    "summary": "OjContestCanlender",
                    "summary_alias": "OjContestCanlender",
                }
            )
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + self.tenant_access_token,
            }
            response = json.loads(
                requests.request("POST", url, headers=headers, data=payload).text
            )
            response_dict = response.json()
            TargetCalanderId = response_dict["calender"]["calendar_id"]

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.tenant_access_token,
        }
        url = (
            "https://open.feishu.cn/open-apis/calendar/v4/calendars/"
            + TargetCalanderId
            + "/events?page_size=500"
        )
        response = requests.request("GET", url, headers=headers)
        response_dict = response.json()
        eventFlag = {}
        for x in response_dict["data"]["items"]:
            if x["status"] == "cancelled":
                pass
            elif x["summary"] not in eventFlag.keys():
                eventFlag[x["summary"]] = x["event_id"]
            else:
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + self.tenant_access_token,
                }
                url = (
                    "https://open.feishu.cn/open-apis/calendar/v4/calendars/"
                    + TargetCalanderId
                    + "/events/"
                    + x["event_id"]
                )
                response = requests.request("DELETE", url, headers=headers)
                # print("DELETE request " + response.json()["msg"])

        for Contest in ContestList:
            payload = json.dumps(
                {
                    "attendee_ability": "can_see_others",
                    "color": 4,
                    "description": Contest["oj"]
                    + ": "
                    + Contest["name"]
                    + "\n"
                    + Contest["link"]
                    + "\n数据来源http://algcontest.rainng.com/",
                    "end_time": {
                        "timestamp": str(Contest["endTimeStamp"]),
                        "timezone": "Asia/Shanghai",
                    },
                    "free_busy_status": "busy",
                    "need_notification": False,
                    "reminders": [{"minutes": 60}],
                    "start_time": {
                        "timestamp": str(Contest["startTimeStamp"]),
                        "timezone": "Asia/Shanghai",
                    },
                    "summary": Contest["oj"] + ": " + Contest["name"],
                    "visibility": "default",
                }
            )
            headers = {
                "Content-Type": "application/json; charset=utf-8",
                "Authorization": "Bearer " + self.tenant_access_token,
            }
            if Contest["oj"] + ": " + Contest["name"] in eventFlag.keys():
                url = (
                    "https://open.feishu.cn/open-apis/calendar/v4/calendars/"
                    + TargetCalanderId
                    + "/events/"
                    + eventFlag[Contest["oj"] + ": " + Contest["name"]]
                )
                response = requests.request("PATCH", url, headers=headers, data=payload)
                # print(response.text)
                CanlanderApiClient._check_error_response(response)
                logging.info("Updated: " + Contest["oj"] + " " + Contest["name"])
            else:
                url = (
                    "https://open.feishu.cn/open-apis/calendar/v4/calendars/"
                    + TargetCalanderId
                    + "/events"
                )
                self._authorize_tenant_access_token()
                response = requests.request("POST", url, headers=headers, data=payload)
                # print(response.text)
                CanlanderApiClient._check_error_response(response)
                AddCnt += 1
                logging.info("Added: " + Contest["oj"] + " " + Contest["name"])

    def _authorize_tenant_access_token(self):
        # get tenant_access_token and set, implemented based on Feishu open api capability. doc link: https://open.feishu.cn/document/ukTMukTMukTM/ukDNz4SO0MjL5QzM/auth-v3/auth/tenant_access_token_internal
        url = "{}{}".format(self._lark_host, TENANT_ACCESS_TOKEN_URI)
        req_body = {"app_id": self._app_id, "app_secret": self._app_secret}
        response = requests.post(url, req_body)
        CanlanderApiClient._check_error_response(response)
        self._tenant_access_token = response.json().get("tenant_access_token")

    @staticmethod
    def _check_error_response(resp):
        # check if the response contains error information
        if resp.status_code != 200:
            resp.raise_for_status()
        response_dict = resp.json()
        code = response_dict.get("code", -1)
        if code != 0:
            logging.error(response_dict)
            raise LarkException(code=code, msg=response_dict.get("msg"))


class LarkException(Exception):
    def __init__(self, code=0, msg=None):
        self.code = code
        self.msg = msg

    def __str__(self) -> str:
        return "{}:{}".format(self.code, self.msg)

    __repr__ = __str__



def GetContestList(url: str = "https://algcontest.rainng.com/") -> list:
    r = requests.get(url)
    if r.status_code == 200:
        return json.loads(r.text)
    return []


def SubscribeCalander():
    url = (
        "https://open.feishu.cn/open-apis/calendar/v4/calendars/:calendar_id/subscribe"
    )
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + USER_ACCESS_TOKEN,
    }
    payload = {
        "calendar_id": "feishu.cn_m6HKXwgZyLDes8qHUZAHad@group.calendar.feishu.cn",
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    # print(response)

def handler(event, context):
    rtndict = {}
    client = CanlanderApiClient(APP_ID, APP_SECRET, LARK_HOST)
    client.update(GetContestList())
    # SubscribeCalander()
    # TelegramBot Report
    if TGBOTENABLE == "ENABLE":
        msg = "Update successfully , adding " + str(AddCnt) + " contest"
        logging.info(msg)
        rtndict["msg"] = msg
        rtndict["type"] = "PLAINTEXT"
        url = f"https://api.telegram.org/bot{TGBOTTOKEN}/sendMessage?chat_id={MASTER_ID}&text={msg}"
        requests.request("Get", url)
    return rtndict

if __name__ == "__main__":
    rtndict = {}
    client = CanlanderApiClient(APP_ID, APP_SECRET, LARK_HOST)
    client.update(GetContestList())
    # SubscribeCalander()
    # TelegramBot Report
    if TGBOTENABLE == "ENABLE":
        msg = "Update successfully , adding " + str(AddCnt) + " contest"
        logging.info(msg)
        rtndict["msg"] = msg
        rtndict["type"] = "PLAINTEXT"
        url = f"https://api.telegram.org/bot{TGBOTTOKEN}/sendMessage?chat_id={MASTER_ID}&text={msg}"
        requests.request("Get", url)