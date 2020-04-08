# Metaflow Automated Credentials Resolver

This allows a service/user/sentient robot to fetch a set of metaflow credentials for an AWS deployed metaflow instance.
It is designed to use the same API key as the Metaflow Metadata Service, allowing robust authentication of incoming clients with 
an already deployed solution.

To use this project, you need to do the following:
1. Package up the credentials-automator lambda into a deployable ZIP and add to S3, (noting the bucket and file path).
2.  Add in several sections to your metaflow cloudformation file (default is here: https://github.com/Netflix/metaflow-tools/blob/master/aws/cloudformation/metaflow-cfn-template.yml)
    These are:
    2.1 Add in the ServerlessApi endpoint, this allows us to use AWS SAM to attach lambda to the API events
    2.2 Add in the API stage for the ServerlessApi (can be configured to your desire), this allows the serverlessApi to use the metaflow api_key to authenticate.
    2.3 Paste in the Lambda Role + Lambda, ensuring that the three parameters are filled correctly (can be found as parameters to api.yml). The Path and Artifacts paramters should point to the noted bucket and file path for lambda deployments.

    An example of this is shown in example.yml (search for 2.1, 2.2 + 2.3). However, I would suggest you use your own version of the metaflow cfn file, as this one may be out of date.


That *should* be it!

You can then hit the deployed API endpoint, passing the API_KEY in the header to validate your client. This will then return you a JSON object with the metaflow credentials encoded for you.