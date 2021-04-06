from os import path
from aws_cdk import core
from aws_cdk import core as cdk
from aws_cdk.aws_events import EventPattern as EventPattern
import aws_cdk.aws_lambda as lambda_
import aws_cdk.aws_events as events
import aws_cdk.aws_sqs as sqs
import aws_cdk.aws_events_targets as targets


class PythonGreenlineStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        this_dir = path.dirname(__file__)

        queue = sqs.Queue(self, "Queue")

        handler = lambda_.Function(self, "Handler",
            runtime=lambda_.Runtime.PYTHON_3_7,
            handler="handler.handler",
            code=lambda_.Code.from_asset(path.join(this_dir, 'lambda')),
            dead_letter_queue=queue,
            max_event_age=cdk.Duration.hours(2), # Otional: set the maxEventAge retry policy
            retry_attempts=2
            )
        
        rule = events.Rule(self, "rule",
           event_pattern=EventPattern(
           source=["aws.ec2"]))

        rule.add_target(targets.LambdaFunction(handler))

