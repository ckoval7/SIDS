#!/usr/bin/env python3

from idService import DoorController
from optparse import OptionParser
import json
import datetime
import sqlite3

host = "172.16.0.206"
user = "root"
password = "badges"

controller1 = DoorController(host, user, password)
database_name = "test1.db"


def createDB():
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS access_points (
        ap_id INTEGER PRIMARY KEY AUTOINCREMENT,
        token TEXT UNIQUE,
        direction INTEGER
        )
    ''')
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_token TEXT UNIQUE,
        first_name TEXT,
        last_name TEXT,
        credential_token TEXT,
        access_profile TEXT,
        status INTEGER,
        last_time_in TEXT,
        last_time_out TEXT
        )
    ''')
    c.execute('''CREATE TABLE IF NOT EXISTS in_out_log (
        log_id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        token TEXT UNIQUE,
        accessGranted INTEGER,
        user_token TEXT,
        access_point TEXT
        )
    ''')
    conn.commit()


def get_accesspoints():
    ap_list = controller1.get_AccessPointList()
    for ap in ap_list["AccessPoint"]:
        token = ap["token"]
        for attribute in ap["Attribute"]:
            if attribute["Name"] == "Direction":
                direction = attribute["Value"]

        conn = sqlite3.connect(database_name)
        c = conn.cursor()
        # c.execute('''INSERT OR REPLACE INTO access_points(token, direction)
        c.execute('''INSERT OR IGNORE INTO access_points(token, direction)
            VALUES(?, ?)''', (token, direction))
        conn.commit()


def get_users():
    users = controller1.get_all_users()
    for user in users["User"]:
        token = user["token"]
        status = "out"
        for attribute in user["Attribute"]:
            if attribute["Name"] == "FirstName":
                fname = attribute["Value"]
            elif attribute["Name"] == "LastName":
                lname = attribute["Value"]

        conn = sqlite3.connect(database_name)
        c = conn.cursor()
        # c.execute('''INSERT OR REPLACE INTO users(user_token, first_name, last_name, status)
        c.execute('''INSERT OR IGNORE INTO users(user_token, first_name, last_name, status)
            VALUES(?, ?, ?, ?)''', (token, fname, lname, status))
        conn.commit()


def log_in_out(log):
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    for entry in log["Event"]:
        token = entry["token"]
        time = entry["UtcTime"]
        for topic in entry["KeyValues"]:
            if topic["Key"] == "AccessPointToken":
                print(topic)
                ap = topic["Value"]

        for topic in entry["KeyValues"]:
            if topic["Value"] == "AccessGranted":
                access = True
                for x in entry["KeyValues"]:
                    if x["Key"] == "CredentialHolderName":
                        print(x)
                        user_token = x["Value"]
                        c.execute('SELECT direction FROM access_points WHERE token=?',
                                  (ap,))
                        status = c.fetchone()[0]
                        if status == "in":
                            c.execute('''UPDATE users SET status = ?,
                                last_time_in = ?
                            WHERE user_token = ?''', (status, time, user_token))
                        elif status == "out":
                            c.execute('''UPDATE users SET status = ?,
                                last_time_out = ?
                            WHERE user_token = ?''', (status, time, user_token))

                        # print(f'Status: {status}')
            elif topic["Value"] == "Denied":
                access = False
                user_token = None
                print("Unknown badge presented!")
        # print(json.dumps(entry, indent=2))
        c.execute('''INSERT OR IGNORE INTO in_out_log(
            timestamp,
            token,
            accessGranted,
            user_token,
            access_point)
            VALUES(?, ?, ?, ?, ?)''', (time, token, access, user_token, ap))
    conn.commit()


if __name__ == '__main__':
    ###############################################
    # Help info printed when calling the program
    ###############################################
    # usage = "usage: %prog -d FILE [options]"
    # parser = OptionParser(usage=usage)
    # parser.add_option("-d", "--database", dest="database_name",
    #                   help="REQUIRED Database File", metavar="FILE")
    #
    # (options, args) = parser.parse_args()
    #
    # mandatories = ['database_name']
    # for m in mandatories:
    #     if options.__dict__[m] is None:
    #         print("You forgot an arguement")
    #         parser.print_help()
    #         exit(-1)

    createDB()
    get_accesspoints()
    get_users()
    start = (datetime.datetime.utcnow().replace(microsecond=0) -
             datetime.timedelta(hours=12)).isoformat()  # "2012-11-27T00:00:00"
    stop = datetime.datetime.utcnow().replace(microsecond=0).isoformat()
    key = "topic0"
    value = "AccessControl"
    log_in_out(controller1.get_EventLog(start, stop, key, value))

# log = controller1.getEventLog(start, stop, key, value)
# # print(json.dumps(log, indent=2))
#
# for entry in log["Event"]:
#     for topic in entry["KeyValues"]:
#         if topic["Value"] == "AccessGranted":
#             for x in entry["KeyValues"]:
#                 if x["Key"] == "CredentialHolderName":
#                     token = x["Value"]
#                     user = controller1.getUser(token)
#                     print(json.dumps(user, indent=2))
#         elif topic["Value"] == "Denied":
#             print(json.dumps(entry, indent=2))
