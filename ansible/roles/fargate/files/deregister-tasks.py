import boto3

client = boto3.client('ecs')

response = client.list_task_definitions(
    familyPrefix='python-sample-app'
)

for r in response['taskDefinitionArns']:
	client.deregister_task_definition(taskDefinition=r)