#!/usr/bin/env python3

from idService import DoorController
import json

host = "172.16.0.206"
user = "root"
password = "badges"

controller1 = DoorController(host, user, password)

print("Unit Tests:")

# print("getControllers:\n")
# print(json.dumps(controller1.getControllers(), indent=2) + "\n\n")

# print("getAccessProfileList:\n")
# access_profile = controller1.getAccessProfileList()
# print(json.dumps(access_profile, indent=2) + "\n\n")

# print("getCredentialList:\n")
# creds = controller1.getCredentialList()
# print(json.dumps(creds, indent=2) + "\n\n")


# # Delete all credentials!
# for cred in creds["Credential"]:
#     print(cred["token"])
#     print(controller1.removeCredential(cred["token"]))

# print("getUsers:\n")
# users = controller1.getUsers()
# print(json.dumps(users, indent=2) + "\n\n")
#
card_num = "8399"
card_hex = "0222419f"

# for user in users["User"]:
# print(controller1.createCredential(card_num, card_hex, users["User"][0]["token"],
#                                    access_profile["AccessProfile"][0]["token"]))


# print("getIdPoints:\n")
# id_points = controller1.getIdPoints()
# print(json.dumps(id_points, indent=2) + "\n\n")

# idp_token = id_points["IdPointInfo"][1]["token"]
# print(controller1.accessRequest(card_hex, idp_token))

#

# print("getAccessPointList:\n")
# print(json.dumps(controller1.getAccessPointList(), indent=2) + "\n\n")

# print("getAuthProfileList:\n")
# print(json.dumps(controller1.getAuthProfileList(), indent=2) + "\n\n")

# print("getDoorConfigurationList:\n")
# print(json.dumps(controller1.getDoorConfigurationList(), indent=2) + "\n\n")

# door_token = controller1.getDoorConfigurationList()["DoorConfiguration"][0]["token"]

# print("getDoorConfiguration:\n")
# print(json.dumps(controller1.getDoorConfiguration(door_token), indent=2) + "\n\n")

# ap_token = "Axis-b8a44f251f8a:1632430108.620177000"
# door_token = "Axis-b8a44f251f8a:1632430106.307029000"
# idpoint_token = "Axis-b8a44f251f8a:1632430106.372559000"
# direction = "out"
# controller1.updateAccessPoint(ap_token, door_token, idpoint_token, direction)
#
# ap_token = "Axis-b8a44f251f8a:1632430108.654372000"
# door_token = "Axis-b8a44f251f8a:1632430106.307029000"
# idpoint_token = "Axis-b8a44f251f8a:1632430106.572800000"
# direction = "in"
# controller1.updateAccessPoint(ap_token, door_token, idpoint_token, direction)

# ap_list = controller1.getAccessPointList()
#
# for ap in ap_list['AccessPoint']:
#     token = ap['token']
#     print(token)
#     controller1.updateAccessPoint(token)

# print("getAccessPointList:\n")
# print(json.dumps(controller1.getAccessPointList(), indent=2) + "\n\n")

# controller1.createAccessProfile("everyone")