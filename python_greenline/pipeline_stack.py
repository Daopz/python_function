from aws_cdk import core
from aws_cdk import core as cdk
from aws_cdk import aws_codepipeline as codepipeline
from aws_cdk import aws_codepipeline_actions as cpactions
from aws_cdk import pipelines



#APP_ACCOUNT = '507856266964'

class PipelineStack(cdk.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        source_artifact = codepipeline.Artifact()
        cloud_assembly_artifact = codepipeline.Artifact()

        pipelines.CdkPipeline(self, 'Pipeline',
          cloud_assembly_artifact=cloud_assembly_artifact,
          pipeline_name='GrennlinePipeline',

          source_action=cpactions.GitHubSourceAction(
            action_name='GitHub',
            output=source_artifact,
            oauth_token=core.SecretValue.secrets_manager('python_token'),
            owner='Daopz',
            branch='main',
            repo='python_function',
            trigger=cpactions.GitHubTrigger.POLL),

        synth_action=pipelines.SimpleSynthAction(
          source_artifact=source_artifact,
          cloud_assembly_artifact=cloud_assembly_artifact,
          install_command='npm install -g aws-cdk && pip install -r requirements.txt',
          synth_command='cdk synth'))


