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


def createGeneric(nifiConfiguration, genricInfo, genericcontent):
    nifiConfiguration.create(genricInfo[env.NAME_TAG], genericcontent)
    for variable in genricInfo[env.VARIABLE_TAG]:
        nifiConfiguration.changeVariable(genricInfo[env.NAME_TAG], variable,
                                         genricInfo[env.VARIABLE_TAG][variable])
