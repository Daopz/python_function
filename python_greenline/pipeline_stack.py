from aws_cdk import core
from aws_cdk import core as cdk
from aws_cdk import aws_codepipeline as codepipeline
from aws_cdk import aws_codepipeline_actions as cpactions
from aws_cdk import pipelines

from .greenline_stage import GrennlineServiceStage

APP_ACCOUNT = '0123456789012'

class PipelineStack(cdk.Stack):

  def __init__(self, scope: core.Construct, id: str, **kwargs):
    super().__init__(scope, id, **kwargs)

    source_artifact = codepipeline.Artifact()
    cloud_assembly_artifact = codepipeline.Artifact()

    pipeline = pipelines.CdkPipeline(self, 'Pipeline',
      cloud_assembly_artifact=cloud_assembly_artifact,
      pipeline_name='GrennlinePipeline',

      source_action=cpactions.GitHubSourceAction(
        action_name='GitHub',
        output=source_artifact,
        oauth_token=core.SecretValue.secrets_manager('Oauth-Token-XXXX'), # Valid Oauth token must put here
        owner='XXXX', #OwnerRepo
        branch='main',
        repo='XXXX', #Name of the Repo
        trigger=cpactions.GitHubTrigger.POLL),

      synth_action=pipelines.SimpleSynthAction(
        source_artifact=source_artifact,
        cloud_assembly_artifact=cloud_assembly_artifact,
        install_command='npm install -g aws-cdk && pip install -r requirements.txt',
        synth_command='cdk synth'))
    
    pre_prod_stage = pipeline.add_application_stage(GrennlineServiceStage(self, 'Pre-Prod', env={
      'account': APP_ACCOUNT,
      'region': 'us-east-1',
    }))

    pre_prod_stage.add_manual_approval_action(
      action_name='PromoteToProd'
    )

    pipeline.add_application_stage(GrennlineServiceStage(self, 'Prod', env={
      'account': APP_ACCOUNT,
      'region': 'us-east-1',
    }))




