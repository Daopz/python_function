from os import path
from aws_cdk import core
from aws_cdk import core as cdk
from aws_cdk.aws_events import EventPattern as EventPattern
import aws_cdk.aws_lambda as lambda_
import aws_cdk.aws_apigateway as apigw
import aws_cdk.aws_codedeploy as codedeploy
import aws_cdk.aws_cloudwatch as cloudwatch
import aws_cdk.aws_events as events
import aws_cdk.aws_sqs as sqs
import aws_cdk.aws_events_targets as targets


class PythonGreenlineStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        this_dir = path.dirname(__file__)

        queue = sqs.Queue(self, "Queue")

        handler = lambda_.Function(self, "Handler",
            runtime=lambda_.Runtime.PYTHON_3_7,
            handler="handler.handler",
            code=lambda_.Code.from_asset(path.join(this_dir, 'lambda')),
            dead_letter_queue=queue,
            max_event_age=cdk.Duration.hours(2), 
            retry_attempts=2
            )
        
        rule = events.Rule(self, "rule",
           event_pattern=EventPattern(
           source=["aws.ec2"]))

        rule.add_target(targets.LambdaFunction(handler))

        alias = lambda_.Alias(self, 'HandlerAlias',
            alias_name='Current',
            version=handler.current_version)


        gw = apigw.LambdaRestApi(self, 'Gateway',
            description='Endpoint for a simple Lambda-powered web service',
            handler=alias)

        failure_alarm = cloudwatch.Alarm(self, 'FailureAlarm',
            metric=cloudwatch.Metric(
                metric_name='5XXError',
                namespace='AWS/ApiGateway',
                dimensions={
                    'ApiName': 'Gateway',
                },
                statistic='Sum',
                period=core.Duration.minutes(1)),
            threshold=1,
            evaluation_periods=1)

        codedeploy.LambdaDeploymentGroup(self, 'DeploymentGroup',
            alias=alias,
            deployment_config=codedeploy.LambdaDeploymentConfig.CANARY_10_PERCENT_10_MINUTES,
            alarms=[failure_alarm])

        self.url_output = core.CfnOutput(self, 'Url',
            value=gw.url)

