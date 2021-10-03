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

        controller = self.getControllers()

        self.token = controller['AccessController'][0]['token']

        self.access_points = self.getAccessPointList()

        self.door_token = self.getDoorConfigurationList()["DoorConfiguration"][0]["token"]

        print(self.token)
        # print(self.access_points)
        print(self.door_token)

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

    def getAuthProfileList(self):
        payload = {"pacsaxis:GetAuthenticationProfileList": {}}

        response = requests.post(self.url + self.acs_path, json=payload,
                                 auth=HTTPDigestAuth(self.user, self.password))

        if response.status_code == 200:
            self.auth_profiles = json.loads(response.text)
        else:
            print(response.text)

        return self.auth_profiles

    def getAccessPointList(self):
        payload = {"pacsaxis:GetAccessPointList": {}}

        response = requests.post(self.url + self.acs_path, json=payload,
                                 auth=HTTPDigestAuth(self.user, self.password))

        if response.status_code == 200:
            self.access_points = json.loads(response.text)
        else:
            print(response.text)

        return self.access_points

    def getDoorConfigurationList(self):
        payload = {"axtdc:GetDoorConfigurationList": {}}

        response = requests.post(self.url + self.door_path, json=payload,
                                 auth=HTTPDigestAuth(self.user, self.password))

        if response.status_code == 200:
            self.doors_config_list = json.loads(response.text)
        else:
            print(response.text)

        return self.doors_config_list

    def getAccessProfileList(self):
        payload = {
            "pacsaxis:GetAccessProfileList": {}
        }

        response = requests.post(self.url + self.acs_path, json=payload,
                                 auth=HTTPDigestAuth(self.user, self.password))

        if response.status_code == 200:
            self.access_profiles = json.loads(response.text)
        else:
            print(response.text)

        return self.access_profiles

    def getCredentialList(self):
        payload = {
            "pacsaxis:GetCredentialList": {}
        }

        response = requests.post(self.url + self.acs_path, json=payload,
                                 auth=HTTPDigestAuth(self.user, self.password))

        if response.status_code == 200:
            self.credentials = json.loads(response.text)
        else:
            print(response.text)

        return self.credentials

    # One AccessPoint object for each direction (in and out) which there are
    # readers/REX devices that allow access in that direction. For example, a
    # door with a reader allowing access going in and a REX device allowing
    # access going out will require two AccessPoints associated with it.
    def updateAccessPoint(self, ap_token, door_token, idpoint_token, direction, auth_profile="CardOnly"):
        payload = {
            "pacsaxis:SetAccessPoint": {
                "AccessPoint": [
                    {
                        "token": ap_token,
                        "Name": "",
                        "Description": "",
                        "AreaFrom": "",
                        "AreaTo": "",
                        "EntityType": "tdc:Door",
                        "Entity": door_token,
                        "Enabled": True,
                        # "DoorDeviceUUID": "6f88f082-2d61-4290-9bc6-b8a44f251f8a",
                        "IdPointDevice": [
                            {
                                "IdPoint": idpoint_token,
                                "DeviceUUID": ""
                            }
                        ],
                        "AuthenticationProfile": [
                            auth_profile
                        ],
                        "Attribute": [
                            {
                                "type": "",
                                "Name": "Direction",
                                "Value": direction
                            }
                        ],
                        "ActionArgument": [],
                        "Action": "Access"
                    },
                ]
            }
        }

        response = requests.post(self.url + self.acs_path, json=payload,
                                 auth=HTTPDigestAuth(self.user, self.password))

        if response.status_code == 200:
            text = json.loads(response.text)
        else:
            print(response.text)

        return text

    def createAccessProfile(self, name, auth_profile="CardOnly"):
        # Access profile = group

        payload = {
            "pacsaxis:SetAccessProfile": {
                "AccessProfile": [
                    {
                        "Name": name,
                        "Description": "",
                        "Enabled": True,
                        "Schedule": [
                            "standard_always"
                        ],
                        "AccessPolicy":[
                            {
                                "Schedule": [
                                    "standard_always"
                                ],
                                "AccessPoint": self.access_points["AccessPoint"][0]["token"],

                            },
                            {
                                "Schedule": [
                                    "standard_always"
                                ],
                                "AccessPoint": self.access_points["AccessPoint"][1]["token"]
                            }
                        ],
                        "Attribute":[],
                        "AuthenticationProfile":[
                            auth_profile
                        ],
                    }
                ]
            }
        }

        response = requests.post(self.url + self.acs_path, json=payload,
                                 auth=HTTPDigestAuth(self.user, self.password))

        if response.status_code == 200:
            text = json.loads(response.text)
        else:
            print(response.text)

        return text

    def createUser(self, fname, lname):
        payload = {
            "axudb:SetUser": {
                "User": [
                  {
                      "Name": f"{lname}, {fname}",
                      "Description": "",
                      "Attribute": [
                          {
                              "type": "string",
                              "Name": "FirstName",
                              "Value": fname
                          },
                          {
                              "type": "string",
                              "Name": "LastName",
                              "Value": lname
                          }
                      ]
                  }
                ]
            }
        }

        response = requests.post(self.url + self.acs_path, json=payload,
                                 auth=HTTPDigestAuth(self.user, self.password))

        if response.status_code == 200:
            self.last_user_token = json.loads(response.text)
        else:
            print(response.text)

        return self.last_user_token

    def createCredential(self, card_num, card_hex, user_token, access_profile):
        payload = {
            "pacsaxis:SetCredential": {
                "Credential": [
                    {
                        "ValidFrom": "1997-01-01T00:00:00Z",
                        "ValidTo": "2038-01-01T00:00:00Z",
                        "Enabled": True,
                        "Status": "Enabled",
                        "IdData": [
                            {
                                "Name": "CardNr",
                                "Value": card_num
                            },
                            {
                                "Name": "Card",
                                "Value": card_hex
                            }
                        ],
                        "CredentialAccessProfile": [{
                            "AccessProfile": access_profile,
                            "ValidFrom": "1997-01-01T00:00:00Z",
                            "ValidTo": "2038-01-01T00:00:00Z",
                        }],
                        "UserToken": user_token
                    }
                ]
            }
        }

        response = requests.post(self.url + self.acs_path, json=payload,
                                 auth=HTTPDigestAuth(self.user, self.password))

        if response.status_code == 200:
            self.last_credential_token = json.loads(response.text)
        else:
            print(response.text)

        return self.last_credential_token

    def removeCredential(self, cred_token):
        payload = {
            "pacsaxis:RemoveCredential": {"Token": [cred_token]}
        }

        response = requests.post(self.url + self.acs_path, json=payload,
                                 auth=HTTPDigestAuth(self.user, self.password))

        if response.status_code == 200:
            return response.text
        else:
            print(response.text)

        # return text

    def accessRequest(self, card_hex, idp_token):
        payload = {
            "pacsaxis:RequestAccess": {
                "Action": "Access",
                "IdData": [{
                    "Name": "Card",
                    "Value": card_hex
                },
                ],
                "SourceToken": idp_token,
                "TargetToken": self.door_token,
                "Token": self.token
            }
        }

        response = requests.post(self.url + self.acs_path, json=payload,
                                 auth=HTTPDigestAuth(self.user, self.password))

        if response.status_code == 200:
            text = json.loads(response.text)
        else:
            print(response.text)

        return text

    def createAuthenticationProfile(self):
        # Each AccessPoint is associated with zero or more AuthenticationProfiles
        # indicating when it is possible to gain access to the door. For each type
        # of IdData in credential (PIN, card, card and PIN, or REX) there is at most
        # one AuthenticationProfile object per AccessPoint.

        payload = {
            "pacsaxis:SetAuthenticationProfile": {
                "AuthenticationProfile": [
                    {
                        "Name": "",
                        "Description": "",
                        "Schedule": [
                            "standard_always"
                        ],
                        # If access should be granted using a card without a
                        # PIN code, one IdFactor is created with IdDataName
                        # set to "CardNr", IdMatchOperatorName set to
                        # "IdDataEqual", and OperatorValue set to "".
                        "IdFactor":[
                            {
                                "IdDataName": "CardNr",
                                "IdMatchOperatorName": "IdDataEqual",
                                "OperatorValue": ""
                            },
                        ]
                    }
                ]
            }
        }

        response = requests.post(self.url + self.acs_path, json=payload,
                                 auth=HTTPDigestAuth(self.user, self.password))

        if response.status_code == 200:
            text = json.loads(response.text)
        else:
            print(response.text)

        return text
