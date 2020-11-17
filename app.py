#!/usr/bin/env python3

import os

import requests
from aws_cdk import core

from geoprocessing_workstation.geoprocessing_workstation_stack import (
    GeoprocessingWorkstationStack,
)


def get_public_ip() -> str:
    return requests.get("https://api.ipify.org?format=json").json()["ip"]


app = core.App()

identifier = os.environ.get("IDENTIFIER", "dev")
GeoprocessingWorkstationStack(
    app,
    f"geoprocessing-workstation-{identifier}",
    identifier=identifier,
    public_ip=get_public_ip(),
)

app.synth()
