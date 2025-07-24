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
import env


def createRucio(nifiConfiguration, ruciopInfo, ruciocontent):
    ruciocontent = rucioPreparefile(ruciocontent, ruciopInfo)
    nifiConfiguration.create(ruciopInfo[env.NAME_TAG], ruciocontent)
    nifiConfiguration.changeVariable(ruciopInfo[env.NAME_TAG], "service_filter",
                                     ruciopInfo[env.RUCIO_SERVICE_FILTER])


def rucioPreparefile(filecontent, rucio):
    filecontent = auxiliaryFunctions.addSensitiveVariable(filecontent, "ConsumeAMQP","Password" , rucio[env.RUCIO_PASSWORD_TAG])
    filecontent = auxiliaryFunctions.addSensitiveVariable(filecontent, "ConsumeAMQP","User Name" , rucio[env.RUCIO_VIRTUAL_HOST_TAG])
    filecontent = auxiliaryFunctions.addSensitiveVariable(filecontent, "ConsumeAMQP","Port" , rucio[env.RUCIO_PORT_TAG])
    filecontent = auxiliaryFunctions.addSensitiveVariable(filecontent, "ConsumeAMQP","Queue" , rucio[env.RUCIO_QUEUE_NAME_TAG])
    filecontent = auxiliaryFunctions.addSensitiveVariable(filecontent, "ConsumeAMQP","Host Name" , rucio[env.RUCIO_HOST_TAG])
    filecontent = auxiliaryFunctions.addSensitiveVariable(filecontent, "ConsumeAMQP","ssl-client-auth" , rucio[env.RUCIO_SSL_CONTEXT_TAG])
    return filecontent
