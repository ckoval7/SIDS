#!/usr/bin/env python3

from idService import DoorController
from optparse import OptionParser
import json
import signal
import datetime
from time import sleep
import sqlite3
import threading
from os import system, name, kill, getpid
from bottle import (route, run, request, get, put, abort, error,
                    response, redirect, template, static_file)

host = "172.16.0.206"
user = "root"
password = "badges"

controller1 = DoorController(host, user, password)
database_name = "test1.db"


###############################################
# Serves static files such as CSS and JS to the
# WebUI
###############################################
@route('/static/<filepath:path>', name='static')
def server_static(filepath):
    response = static_file(filepath, root='./static')
    response.set_header(
        'Cache-Control', 'no-cache, no-store, must-revalidate, max-age=0')
    return response


###############################################
# Loads the main page of the WebUI
# http://[ip]:[port]/
###############################################
@get('/')
@get('/index')
def serve_page():
    return template('index.tpl')


@get('/whoshere')
def whos_here():
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    c.execute('SELECT first_name, last_name, last_time_in FROM users WHERE status="in"')
    users = c.fetchall()
    # print(users)
    # return "OK"
    return template('whoshere.tpl', {'users': users})


@get('/entrylog')
def entry_log():
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    c.execute('''SELECT
                    users.last_name AS last_name,
                    users.first_name AS first_name,
                    access_points.direction AS direction,
                    timestamp
                FROM in_out_log
                LEFT JOIN users ON users.user_id = in_out_log.user_id
                LEFT JOIN access_points ON access_points.ap_id = in_out_log.ap_id
                ORDER BY timestamp DESC''')
    log = c.fetchall()
    return template('entrylog.tpl', {'log': log})


@get('/profile')
def list_users():
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    c.execute('''SELECT
                    users.first_name,
                    users.last_name,
                    credentials.card_number,
                    users.user_id
                FROM credentials
                JOIN users ON users.user_id = credentials.user_id''')
    users = c.fetchall()
    log = None
    if users:
        return template('profile.tpl', {'user_info': users,
                                        'log': log})
    else:
        abort(404, "Error, user not found!")


@get('/profile/<badge_number>')
def show_user(badge_number):
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    c.execute('''SELECT
                    users.first_name,
                    users.last_name,
                    credentials.card_number,
                    users.user_id
                FROM credentials
                JOIN users ON users.user_id = credentials.user_id
                WHERE card_number = ?''', (badge_number,))
    users = c.fetchall()
    if users:
        user_id = users[0][3]
        c.execute('''SELECT
                        access_points.direction AS direction,
                        timestamp
                    FROM in_out_log
                    JOIN access_points ON access_points.ap_id = in_out_log.ap_id
                    WHERE user_id = ?
                    ORDER BY timestamp DESC''', (user_id,))
        log = c.fetchall()
        # print(users)
        # return "OK"
        return template('profile.tpl', {'user_info': users,
                                        'log': log})
    else:
        abort(404, "Error, user not found!")


@put('/adduser')
def create_user():
    # return "OK"
    data = json.load(request.body)
    fname = data['fname']
    lname = data['lname']
    card_num = data['cardNum']
    card_hex = data['cardHex']
    access_profile = controller1.get_AccessProfileList()["AccessProfile"][0]["token"]

    user_token = controller1.create_user(fname, lname)["Token"][0]
    # user_token["Token"][0]
    cred_token = controller1.create_Credential(card_num, card_hex, user_token, access_profile)
    get_users()
    get_credentials()
    print(f"Added new user: {fname} {lname}, {user_token}")
    return cred_token


@put('/lookupbadge')
def get_user_by_badge_hex():
    data = json.load(request.body)
    card_hex = data['cardHex']
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    c.execute('''SELECT card_number FROM credentials WHERE card_hex = ?''',
              (card_hex,))

    card_num = c.fetchone()
    if card_num is not None:
        return f'/profile/{card_num[0]}'
    else:
        return '/profile/0'
    #     abort(404, "Error, user not found!")


@put('/lookupname')
def get_user_by_name():
    data = json.load(request.body)
    fname = data['fname']
    lname = data['lname']
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    c.execute('''SELECT
                    card_number
                FROM credentials
                JOIN users ON users.user_id = credentials.user_id
                WHERE users.first_name = ? AND users.last_name = ?''',
              (fname, lname))
    user = c.fetchone()
    if user is not None:
        return f'/profile/{user[0]}'
    else:
        return '/profile/0'


@error(404)
def error404(error):
    return template('404.tpl', {'error': error})


def createDB():
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS doors (
        door_id INTEGER PRIMARY KEY AUTOINCREMENT,
        token TEXT UNIQUE,
        name TEXT,
        host TEXT,
        password TEXT
        )
    ''')
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
        badge_color TEXT,
        credential_token TEXT,
        access_profile TEXT,
        status INTEGER,
        last_time_in TEXT,
        last_time_out TEXT
        )
    ''')
    c.execute('''CREATE TABLE IF NOT EXISTS credentials (
        credential_id INTEGER PRIMARY KEY AUTOINCREMENT,
        credential_token TEXT UNIQUE,
        valid_from TEXT,
        valid_to TEXT,
        enabled INTEGER,
        card_number INTEGER,
        card_hex TEXT,
        user_id,
        FOREIGN KEY (user_id)
            REFERENCES users (user_id)
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS in_out_log (
        log_id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        token TEXT UNIQUE,
        accessGranted INTEGER,
        user_id INTEGER,
        ap_id INTEGER,
        FOREIGN KEY (user_id)
            REFERENCES users (user_id),
        FOREIGN KEY (ap_id)
            REFERENCES access_points (ap_id)
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


def get_credentials():
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    credentials = controller1.get_CredentialList()
    for credential in credentials["Credential"]:
        token = credential["token"]
        user_token = credential["UserToken"]
        valid_from = credential["ValidFrom"]
        valid_to = credential["ValidTo"]
        enabled = credential["Enabled"]
        for item in credential["IdData"]:
            if item["Name"] == "CardNr":
                card_number = item["Value"]

            if item["Name"] == "Card":
                card_hex = item["Value"]

        c.execute('SELECT user_id FROM users WHERE user_token = ?',
                  (user_token,))
        user_id = c.fetchone()[0]

        # credential_id INTEGER PRIMARY KEY AUTOINCREMENT,
        # credential_token TEXT,
        # valid_from TEXT,
        # valid_to TEXT,
        # enabled INTEGER,
        # card_number INTEGER,
        # card_hex TEXT,
        # user_id

        c.execute('''INSERT OR IGNORE INTO credentials(credential_token, valid_from,
            valid_to, enabled, card_number, card_hex, user_id)
            VALUES(?, ?, ?, ?, ?, ?, ?)''',
                  (token, valid_from, valid_to, enabled,
                   card_number, card_hex, user_id))

    conn.commit()


def log_in_out(log):
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    for entry in log["Event"]:
        token = entry["token"]
        time = entry["UtcTime"]
        for topic in entry["KeyValues"]:
            if topic["Key"] == "AccessPointToken":
                # print(topic)
                ap = topic["Value"]
                c.execute('SELECT direction, ap_id FROM access_points WHERE token=?',
                          (ap,))
                ap_result = c.fetchone()
                status = ap_result[0]
                ap_id = ap_result[1]

        for topic in entry["KeyValues"]:
            if topic["Value"] == "AccessGranted":
                access = True
                for x in entry["KeyValues"]:
                    if x["Key"] == "CredentialHolderName":
                        # print(x)
                        user_token = x["Value"]
                        c.execute('SELECT user_id FROM users WHERE user_token = ?',
                                  (user_token,))
                        user_id = c.fetchone()[0]
                        if status == "in":
                            c.execute('''UPDATE users SET status = ?,
                                last_time_in = ?
                            WHERE user_id = ?''', (status, time, user_id))
                        elif status == "out":
                            c.execute('''UPDATE users SET status = ?,
                                last_time_out = ?
                            WHERE user_id = ?''', (status, time, user_id))

                        # print(f'Status: {status}')
            elif topic["Value"] == "Denied":
                access = False
                user_id = None
                # print("Unknown badge presented!")
        # print(json.dumps(entry, indent=2))
        c.execute('''INSERT OR IGNORE INTO in_out_log(
            timestamp,
            token,
            accessGranted,
            user_id,
            ap_id)
            VALUES(?, ?, ?, ?, ?)''', (time, token, access, user_id, ap_id))
    conn.commit()


def get_last_log_time():
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    c.execute('SELECT timestamp FROM in_out_log ORDER BY timestamp DESC LIMIT 1')
    date = c.fetchone()
    if date:
        return date[0]
    else:
        return (datetime.datetime.utcnow().replace(microsecond=0) -
                datetime.timedelta(minutes=1)).isoformat()


###############################################
# Starts the Bottle webserver.
###############################################
def start_server(ipaddr="127.0.0.1", port=8080):
    try:
        run(host=ipaddr, port=port, quiet=True,
            server='paste', debug=True)
    except OSError:
        print(f"Port {port} seems to be in use. Please select another port or " +
              "check if another instance of DFA is already running.")
        # debugging = True
        finish()


###############################################
# Thangs to do before closing the program.
###############################################
def finish():
    # clear(debugging)
    print("Exiting, please wait.\n")
    kill(getpid(), signal.SIGTERM)


if __name__ == '__main__':
    ###############################################
    # Help info printed when calling the program
    ###############################################
    usage = "usage: %prog -d FILE [options]"
    parser = OptionParser(usage=usage)
    parser.add_option("-d", "--database", dest="database_name",
                      help="REQUIRED Database File", metavar="FILE")
    parser.add_option("--ip", dest="ipaddr", help="IP Address to serve from. Default 127.0.0.1",
                      metavar="IP ADDRESS", type="str", default="127.0.0.1")
    parser.add_option("--port", dest="port", help="Port number to serve from. Default 8080",
                      metavar="NUMBER", type="int", default=8080)

    (options, args) = parser.parse_args()

    # mandatories = ['database_name']
    # for m in mandatories:
    #     if options.__dict__[m] is None:
    #         print("You forgot an arguement")
    #         parser.print_help()
    #         exit(-1)

    web = threading.Thread(target=start_server, args=(options.ipaddr, options.port))
    web.daemon = True
    web.start()

    try:
        createDB()
        get_accesspoints()
        get_users()
        get_credentials()
        key = "topic0"
        value = "AccessControl"
        start = (datetime.datetime.utcnow().replace(microsecond=0) -
                 datetime.timedelta(hours=24)).isoformat()  # "2012-11-27T00:00:00"
        stop = datetime.datetime.utcnow().replace(microsecond=0).isoformat()
        log_in_out(controller1.get_EventLog(start, stop, key, value))

        while True:
            sleep(10)
            # start = (datetime.datetime.utcnow().replace(microsecond=0) -
            #          datetime.timedelta(minutes=1)).isoformat()  # "2012-11-27T00:00:00"
            start = get_last_log_time()
            stop = datetime.datetime.utcnow().replace(microsecond=0).isoformat()
            log_in_out(controller1.get_EventLog(start, stop, key, value))

    except KeyboardInterrupt:
        finish()

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
