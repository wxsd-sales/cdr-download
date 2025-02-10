import os
from dotenv import load_dotenv
load_dotenv()

import requests
import sqlite3
import time
import traceback

from datetime import datetime, timedelta

CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
REFRESH_TOKEN = os.environ.get("REFRESH_TOKEN")
WRITE_PATH = os.environ.get("WRITE_PATH")

seconds_ago = 305 #API won't allow for a search more recently than 5 minutes, so we do 5 minutes and 5 seconds just to avoid errors (305 seconds).
webex_api_url = "https://analytics.webexapis.com/v1/cdr_feed?startTime={0}&endTime={1}"

def print_response_error(label, resp):
    print(f"{label}, Code: {resp.status_code}")
    try:
        print(resp.json())
    except Exception as e:
        traceback.print_exc()

class MyData(object):
    ID = 0
    RECORD_TIME = 1
    TOKEN = 2
    TOKEN_REFRESH_TIME = 3

    def __init__(self):
        self.con = sqlite3.connect("main.db")
        self.cur = self.con.cursor()

        res = self.cur.execute("SELECT * FROM sqlite_master")
        tables = res.fetchone()
        if tables == None or 'lastRecord' not in tables:
            self.cur.execute("CREATE TABLE lastRecord(id, record_time, token, token_refresh_time)")
            self.cur.execute(f"INSERT INTO lastRecord VALUES (1, '', '', 0)")
            self.con.commit()
        res = self.cur.execute("SELECT * FROM lastRecord")
        self.record = res.fetchone()
        print('last record:', self.record)
        if self.record[self.TOKEN] == '' or self.record[self.TOKEN_REFRESH_TIME] < time.time()-600:
            print("Refreshing access token...")
            result = self.refresh_token()
            update_statement = "UPDATE lastRecord SET token=?, token_refresh_time=? WHERE id=1"
            self.cur.execute(update_statement, (result['access_token'], time.time()))
            self.con.commit()
            res = self.cur.execute("SELECT * FROM lastRecord")
            self.record = res.fetchone()
            print('last record:', self.record)
        print(self.record[self.TOKEN])

    def refresh_token(self):
        data = {"grant_type": "refresh_token",
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "refresh_token": REFRESH_TOKEN }
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        resp = requests.post("https://webexapis.com/v1/access_token", data=data, headers=headers)
        result = resp.json()
        print(result)
        return result
    
    def get_cdrs(self):
        start_index = 0
        if self.record[self.RECORD_TIME]:
            start_index = 1
            start_time = self.record[self.RECORD_TIME]
        else:
            start_time = (datetime.utcnow() - timedelta(seconds=86400)).isoformat()[:-3]+"Z"
        cdrs = []
        end_time = (datetime.utcnow() - timedelta(seconds=seconds_ago)).isoformat()[:-3]+"Z"
        print('start_time', start_time)
        print('end_time', end_time)
        headers = {"Content-Type":"application/json", "Authorization":f"Bearer {self.record[self.TOKEN]}"}
        cdr_resp = requests.get(webex_api_url.format(start_time, end_time), headers=headers)
        if cdr_resp.status_code == 200:
            cdrs = cdr_resp.json()["items"]
            if len(cdrs) > 0:
                keys = sorted(cdrs[0].keys())
                print("CDR Keys:", keys)
                print("Num CDRS:", len(cdrs))
                last_report_time = cdrs[-1]["Report time"]
                print('last_report_time', last_report_time)
                if len(cdrs[start_index:]) > 0:
                    report_name = last_report_time.replace("-","").replace("T","").replace(":","").replace("Z","").replace(".","_") + ".csv"
                    with open(os.path.join(WRITE_PATH, report_name), "w") as f:
                        f.write(",".join(keys)+",\n")
                        for cdr in cdrs[start_index:]:
                            write_line = ""
                            for key in keys:
                                write_line += f"{cdr[key]},"
                            write_line = write_line[:-1] + "\n"
                            f.write(write_line)
                            print("CDR:", write_line)
                if last_report_time != start_time:
                    update_statement = "UPDATE lastRecord SET record_time=? WHERE id=1"
                    self.cur.execute(update_statement, (last_report_time,))
                    self.con.commit()
                    res = self.cur.execute("SELECT * FROM lastRecord")
                    self.record = res.fetchone()
                    print('last record:', self.record)
        else:
            print_response_error(f"GET CDR Error {start_time}", cdr_resp)
        return cdrs




if __name__ == "__main__":
    try:
        os.makedirs(WRITE_PATH)
    except Exception as e:
        print(e)
    data = MyData()
    data.get_cdrs()

