import boto3
import logging
import json
import os

from exception import LambdaException

logger = logging.getLogger()
logger.setLevel(logging.INFO)

cloudformation_client = boto3.client('cloudformation')

METAFLOW_STACK = os.environ['METAFLOW_STACK']

# Mapping between cloudformation outputs and Metaflow environment variables from default metaflow stack.
# Can be found here: https://github.com/Netflix/metaflow-tools/blob/master/aws/cloudformation/metaflow-cfn-template.yml
default_mapping = {
    "ECSJobRoleForBatchJobs": "METAFLOW_ECS_S3_ACCESS_IAM_ROLE",
    "MetaflowDataStoreS3Url": "METAFLOW_DATASTORE_SYSROOT_S3",
    "BatchJobQueueArn": "METAFLOW_BATCH_JOB_QUEUE",
    "ServiceUrl": "METAFLOW_SERVICE_URL"
}


def lambda_handler(event, context):

    try:
        api_key = event['headers']['x-api-key']

        data = ConfigFactory(api_key, METAFLOW_STACK,
                             default_mapping).get_config()

    except LambdaException as e:
        return {
            "statusCode": e.http_code,
            "body": json.dumps("")
        }
    except Exception as e:
        logger.error(str(e))
        return {
            "statusCode": 500,
            "body": json.dumps(str(e))
        }

    return {
        "statusCode": 200,
        "body": json.dumps(data)
    }


class ConfigFactory():

    def __init__(self, api_key, stack_name, stack_output_mappings):
        self._api_key = api_key
        self._stack_name = stack_name
        self._stack_output_mappings = stack_output_mappings

    def get_config(self):

        try:

            params = self._get_stack_output(_stack_name, stack_output_mappings.keys())

        except:
            raise LambdaException("Not found", 404)

        transformed = {}

        for key, value in params.items():
            transformed[self._stack_output_mappings[key]] = value

        # Concatenate objects
        return {
            **{
                "METAFLOW_DEFAULT_DATASTORE": "s3",
                "METAFLOW_DEFAULT_METADATA": "service"
            },
            **transformed,
            **{
                "METAFLOW_SERVICE_AUTH_KEY": self._api_key
            }
        }

    def _get_stack_output(self, stack_name, params):

        vals = {}

        response = cloudformation_client.describe_stacks(
            StackName=stack_name
        )

        stack_outputs = response['Stacks'][0]

        if 'Outputs' in stack_outputs:

            for output in stack_outputs['Outputs']:
                if output['OutputKey'] in params:

                    index = params.index(output['OutputKey'])
                    vals[params[index]] = output['OutputValue']

        return vals
