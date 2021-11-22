#!/usr/bin/env python3
import os

from aws_cdk import core as cdk

# For consistency with TypeScript code, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core

from stacks.datalake.stack import DataLakeStack
from stacks.kinesis.stack import KinesisStack
from stacks.network.stack import NetworkStack

env = os.environ["ENVIRONMENT"]

app = core.App()
datalake_stack = DataLakeStack(app, deploy_env=env)
kinesis_stack = KinesisStack (
    app, 
    deploy_env=env,
    raw_bucket=datalake_stack.datalake_raw_bucket
)
rds_stack = NetworkStack (
    app, 
    deploy_env=env
)

app.synth()
