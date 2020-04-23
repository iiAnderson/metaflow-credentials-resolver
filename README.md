# Metaflow Automated Credentials Resolver

This allows a service/user/sentient robot to fetch a set of metaflow credentials for an AWS deployed metaflow instance.
It is designed to use the same API key as the Metaflow Metadata Service, allowing robust authentication of incoming clients with 
an already deployed solution.

To use this project, you need to do the following:
1. Package up the credentials-automator lambda into a deployable ZIP and add to S3, (noting the bucket and file path).
2. Deploy the metaflow stack provided by netflix, noting down the ApiKeyId Output and Stack Name.
3. Deploy the api.yml cloudformation file provided here, passing the following parameters:
    a. ConfigAutomatorLambdaPath: The path to the credentials-automator zip you just put into S3 (just file path)
    b. ArtifactBucket: The name of the bucket the zip is uploaded to
    c. MetaflowApiKey: The ApiKeyId outputted from the metaflow stack (can be a placeholder value if not used)
    d. APIBasicAuth: true/false value to enable use of API key


That *should* be it!

You can then hit the deployed API endpoint, passing the API_KEY in the header to validate your client. This will then return you a JSON object with the metaflow credentials encoded for you.