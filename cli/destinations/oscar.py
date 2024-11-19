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
import env


def createOSCAR(nifiConfiguration,oscarInfo,oscarcontent):
    nifiConfiguration.create(oscarInfo[env.NAME_TAG], oscarcontent)
    nifiConfiguration.changeVariable(oscarInfo[env.NAME_TAG], "endpoint",
                        oscarInfo[env.OSCAR_ENDPOINT_TAG])
    nifiConfiguration.changeVariable(oscarInfo[env.NAME_TAG], "service",
                        oscarInfo[env.OSCAR_SERVICE_TAG])
    if env.OSCAR_USER_TAG in oscarInfo and env.OSCAR_PASSWORD_TAG in oscarInfo:
        client = Client("cluster-id", oscarInfo[env.OSCAR_ENDPOINT_TAG],
                        oscarInfo[env.OSCAR_USER_TAG], oscarInfo[env.OSCAR_PASSWORD_TAG], True)
        service = client.get_service(oscarInfo[env.OSCAR_SERVICE_TAG])
        token = service.json()["token"]
        nifiConfiguration.changeVariable(oscarInfo[env.NAME_TAG], "token", token)
    else:
        nifiConfiguration.changeVariable(oscarInfo[env.NAME_TAG], "token",
                            oscarInfo[env.OSCAR_TOKEN_TAG])