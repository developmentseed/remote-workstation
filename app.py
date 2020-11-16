#!/usr/bin/env python3

from aws_cdk import core

from geoprocessing_workstation.geoprocessing_workstation_stack import GeoprocessingWorkstationStack


app = core.App()
GeoprocessingWorkstationStack(app, "geoprocessing-workstation")

app.synth()
