# dCNiOs
# Copyright (C) 2023 - GRyCAP - Universitat Politecnica de Valencia
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the Apache 2.0 Licence as published by
# the Apache Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# Apache 2.0 License for more details.
#
# You should have received a copy of the Apache 2.0 License
# along with this program.  If not, see <https://www.apache.org/licenses/>.

# !/usr/bin/env python3

from apis import auxiliaryFunctions
from apis import nifiManagment
from oscar_python.client import Client



def createOSCAR(nifiConfiguration,oscarInfo,oscarcontent):
    nifiConfiguration.create(oscarInfo["name"], oscarcontent)
    nifiConfiguration.changeVariable(oscarInfo["name"], "endpoint",
                        oscarInfo["endpoint"])
    nifiConfiguration.changeVariable(oscarInfo["name"], "service",
                        oscarInfo["service"])
    if "user" in oscarInfo and "password" in oscarInfo:
        client = Client("cluster-id", oscarInfo["endpoint"],
                        oscarInfo["user"], oscarInfo["password"], True)
        service = client.get_service(oscarInfo["service"])
        token = service.json()["token"]
        nifiConfiguration.changeVariable(oscarInfo["name"], "token", token)
    else:
        nifiConfiguration.changeVariable(oscarInfo["name"], "token",
                            oscarInfo["token"])