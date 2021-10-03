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

access_profile = controller1.getAccessProfileList()["AccessProfile"][0]["token"]


def createUser():
    fname = input("First Name: ")
    lname = input("Last Name: ")
    user_token = controller1.createUser(fname, lname)
    return user_token["Token"][0]


def SetCredential(user_token, access_profile):
    card_num = input("Enter Badge Number: ")
    card_hex = getpass("Swipe Badge on Reader")
    return controller1.createCredential(card_num, card_hex, user_token, access_profile)


def testCredential():
    card_hex = getpass("Swipe Badge on Reader")
    id_points = controller1.getIdPoints()
    idp_token = id_points["IdPointInfo"][1]["token"]
    return controller1.accessRequest(card_hex, idp_token)

# # Delete all credentials!
# for cred in creds["Credential"]:
#     print(cred["token"])
#     print(controller1.removeCredential(cred["token"]))


try:
    user_token = createUser()
    print(SetCredential(user_token, access_profile))
except Exception as e:
    print("Enrollment Error!")
    print(e)
    quit()


print("Enrollment Success")

print("Testing credentials")
print(testCredential())
