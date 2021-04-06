#!/usr/bin/env python3
import os
from aws_cdk import core as cdk
from aws_cdk import core
from python_greenline.python_greenline_stack import PythonGreenlineStack
from python_greenline.pipeline_stack import PipelineStack

PIPELINE_ACCOUNT = '507856266964'

app = core.App()
PythonGreenlineStack(app, "PythonGreenlineStack")

PythonGreenlineStack(app, "PipelineStack", env={
  'account': PIPELINE_ACCOUNT,
  'region': 'us-east-1',

})

app.synth()
