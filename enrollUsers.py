#!/usr/bin/env python3

from idService import DoorController
from getpass import getpass
# import json

host = "172.16.0.206"
user = "root"
password = "badges"

# Create user
# Get First name,
# Get last name
# Save Token

# Create Credential
# Get Card Number
# Swipe Card


controller1 = DoorController(host, user, password)

access_profile = controller1.get_AccessProfileList()["AccessProfile"][0]["token"]


def createUser():
    fname = input("First Name: ")
    lname = input("Last Name: ")
    user_token = controller1.create_user(fname, lname)
    return user_token["Token"][0]


def setCredential(user_token, access_profile):
    card_num = input("Enter Badge Number: ")
    card_hex = getpass("Swipe Badge on Reader")
    return controller1.create_Credential(card_num, card_hex, user_token, access_profile)


def testCredential():
    card_hex = getpass("Swipe Badge on Reader")
    id_points = controller1.get_IdPoints()
    idp_token = id_points["IdPointInfo"][1]["token"]
    return controller1.access_request(card_hex, idp_token)

# # Delete all credentials!
# for cred in creds["Credential"]:
#     print(cred["token"])
#     print(controller1.removeCredential(cred["token"]))


while True:
    try:
        user_token = createUser()
        print(setCredential(user_token, access_profile))
    except Exception as e:
        print("Enrollment Error!")
        print(e)
        quit(-1)

    print("Enrollment Success")

    print("Testing credentials")
    print(testCredential())
    more = input("Enroll another? [Y/n]: ")
    no = ["n", "N", "no", "No", "NO"]
    if more in no:
        quit(1)
