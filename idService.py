#!/usr/bin/env python3

import json
import requests
from requests.auth import HTTPDigestAuth

# user = "root"
# password = "badges"
#
# base_url = "http://172.16.0.206"

entry_idPoint = "Axis-b8a44f251f8a:1632430106.372559000"
exit_idPoint = "Axis-b8a44f251f8a:1632430106.572800000"


class DoorController:
    acs_path = "/vapix/pacs"
    door_path = "/vapix/doorcontrol"
    idPoint_path = "/vapix/idpoint"

    def __init__(self, host, user, password, secure=False):
        self.user = user
        self.password = password
        self.host = host

        if secure:
            self.url = "https://" + self.host
        else:
            self.url = "http://" + self.host

    #####################################
    # Returns a list of door controllers and their access points
    #####################################
    def getControllers(self):
        payload = {"pacsaxis:GetAccessControllerList": {}}

        response = requests.post(self.url + self.acs_path, json=payload,
                                 auth=HTTPDigestAuth(self.user, self.password))

        if response.status_code == 200:
            self.controllers = json.loads(response.text)
        else:
            print(response.text)

        return self.controllers

    #####################################
    # Returns a list of users
    #####################################
    def getUsers(self):
        payload = {"axudb:GetUserList": {}}
        response = requests.post(self.url + self.acs_path, json=payload,
                                 auth=HTTPDigestAuth(self.user, self.password))

        if response.status_code == 200:
            self.users = json.loads(response.text)
        else:
            print(response.text)

        return self.users

    #####################################
    # Returns a list of IdPoints (badge readers)
    #####################################
    def getIdPoints(self):
        payload = {"axtid:GetIdPointInfoList": {}}

        response = requests.post(self.url + self.idPoint_path, json=payload,
                                 auth=HTTPDigestAuth(self.user, self.password))

        if response.status_code == 200:
            self.idPoints = json.loads(response.text)
        else:
            print(response.text)

        return self.idPoints


# def createUser(fname, lname):
#     payload = {
#         "axudb:SetUser": {
#             "User": [
#               {
#                   "Name": f"{lname}, {fname}",
#                   "Description": "",
#                   "Attribute": [
#                       {
#                           "type": "string",
#                           "Name": "FirstName",
#                           "Value": fname
#                       },
#                       {
#                           "type": "string",
#                           "Name": "LastName",
#                           "Value": lname
#                       }
#                   ]
#               }
#             ]
#         }
#     }
#
#     response = requests.post(base_url + acs_path, json=payload,
#                              auth=HTTPDigestAuth(user, password))
#
#     if response.status_code == 200:
#         return response.text
#     else:
#         print(response.text)


#
#
# def createCredential(card_num, user_token, access_profile):
#     payload = {
#         "pacsaxis:SetCredential": {
#             "Credential": [
#                 {
#                     "Enabled": True,
#                     "Status": "Enabled",
#                     "IdData": [
#                         # {
#                         #   "Name":"PIN",
#                         #   "Value":"1234"
#                         # },
#                         {
#                             "Name": "CardNr",
#                             "Value": card_num
#                         }
#                     ],
#                     "CredentialAccessProfile": [{
#                         "AccessProfile": access_profile,
#                         "ValidFrom": "",
#                         "ValidTo": "",
#                     }],
#                     "UserToken": user_token
#                 }
#             ]
#         }
#     }
#
#     response = requests.post(base_url + acs_path, json=payload,
#                              auth=HTTPDigestAuth(user, password))
#
#     if response.status_code == 200:
#         return response.text
#     else:
#         print(response.text)
#
#
# def createAuthenticationProfile():
#     # Each AccessPoint is associated with zero or more AuthenticationProfiles
#     # indicating when it is possible to gain access to the door. For each type
#     # of IdData in credential (PIN, card, card and PIN, or REX) there is at most
#     # one AuthenticationProfile object per AccessPoint.
#
#     payload = {
#         "pacsaxis:SetAuthenticationProfile": {
#             "AuthenticationProfile": [
#                 {
#                     "Name": "",
#                     "Description": "",
#                     "Schedule": [
#                         "standard_always"
#                     ],
#                     # If access should be granted using a card without a
#                     # PIN code, one IdFactor is created with IdDataName
#                     # set to "CardNr", IdMatchOperatorName set to
#                     # "IdDataEqual", and OperatorValue set to "".
#                     "IdFactor":[
#                         {
#                             "IdDataName": "CardNr",
#                             "IdMatchOperatorName": "IdDataEqual",
#                             "OperatorValue": ""
#                         },
#                     ]
#                 }
#             ]
#         }
#     }
#
#
# def updateAccessPoint(auth_profile, ap_token):
#     # One AccessPoint object for each direction (in and out) which there are
#     # readers/REX devices that allow access in that direction. For example, a
#     # door with a reader allowing access going in and a REX device allowing
#     # access going out will require two AccessPoints associated with it.
#     payload = {
#         "pacsaxis:SetAccessPoint": {
#             "AccessPoint": [
#                 {
#                     "EntityType": "axtdc:Door",
#                     # "Name":"Front door",
#                     # "Enabled":true,
#                     # "Action":"AccessDoor",
#                     "AuthenticationProfile": [
#                         auth_profile
#                     ],
#                     "Entity":"Axis-00408c184bd9:1350969415.227159000",
#                     "Attribute":[
#                         {
#                             "type": "",
#                             "Name": "Direction",
#                             "Value": "in"
#                         }
#                     ],
#                     "IdPointDevice": [
#                         {
#                             "IdPoint": "Axis-00408c184bd9:1350969415.294313000",
#                             "DeviceUUID": ""
#                         }
#                     ],
#                     "token": ap_token,  # "Axis-00408c184bd9:1350969417.922694000",
#                     # "Description": "",
#                     # "DoorDeviceUUID": "5581ad80-95b0-11e0-b883-00408c184bd9"
#                 }
#             ]
#         }
#     }
#
#
# def createAccessProfile(name, access_point):
#     # Access profile = group
#
#     payload = {
#         "pacsaxis:SetAccessProfile": {
#             "AccessProfile": [
#                 {
#                     "Name": name,
#                     "Description": "",
#                     "Enabled": True,
#                     "Schedule": [],
#                     "AccessPolicy":[
#                         {
#                             "Schedule": [
#                                 "standard_always"
#                             ],
#                             "AccessPoint":"Axis-b8a44f251f8a:1632430108.654372000",
#
#                         },
#                         {
#                             "Schedule": [
#                                 "standard_always"
#                             ],
#                             "AccessPoint":"Axis-b8a44f251f8a:1632430108.620177000"
#                         }
#                     ],
#                     "Attribute":[],
#                     "AuthenticationProfile":[],
#                 }
#             ]
#         }
#     }


# print(createAuthenticationProfile())
#
# print(getControllers())
#
# payload = {"axtid:GetIdPointInfoList": {}}
#
# response = requests.post(base_url + idPoint_path, json=payload,
#                          auth=HTTPDigestAuth(user, password))
#
# print(response.text)
# def main():
#     print(getUsers())
#
#
# if __name__ == "__main__":
#     main()
