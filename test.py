#!/usr/bin/env python3

from idService import DoorController
import json

host = "172.16.0.206"
user = "root"
password = "badges"

controller1 = DoorController(host, user, password)

print("Unit Tests:")

print("getControllers:\n")
print(json.dumps(controller1.getControllers(), indent=2) + "\n\n")

print("getUsers:\n")
print(json.dumps(controller1.getUsers(), indent=2) + "\n\n")

print("getIdPoints:\n")
print(json.dumps(controller1.getIdPoints(), indent=2) + "\n\n")
