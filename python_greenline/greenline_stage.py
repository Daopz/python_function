from aws_cdk import core

from .python_greenline_stack import PythonGreenlineStack

class GrennlineServiceStage(core.Stage):
  def __init__(self, scope: core.Construct, id: str, **kwargs):
    super().__init__(scope, id, **kwargs)

    service = PythonGreenlineStack(self, 'GreenlineService')

    