#!/usr/bin/env python3

import os

import requests
from aws_cdk import core
from stringcase import pascalcase

from remote_workstation.remote_workstation_stack import RemoteWorkstationStack


def get_public_ip() -> str:
    return requests.get("https://api.ipify.org?format=json").json()["ip"]


app = core.App()

identifier = os.environ.get("IDENTIFIER", "dev")
RemoteWorkstationStack(
    app,
    f"remote-workstation-{identifier}",
    identifier=identifier,
    public_ip=get_public_ip(),
)

tags = [
    (pascalcase(item[0].replace("TAGS_", "").lower()), item[1])
    for item in os.environ.items()
    if item[0].startswith("TAGS_")
]

for k, v in tags:
    core.Tags.of(app).add(k, v, apply_to_launched_instances=True)

app.synth()
