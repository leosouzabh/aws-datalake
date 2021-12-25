import json
import boto3

client = boto3.client('secretsmanager')


secret = client.list_secrets()['SecretList'][0]
response = client.get_secret_value(
    SecretId=secret['Name']
)

dbCreds = json.loads(response["SecretString"])
print(f"""

URL     = {dbCreds['host']}:{dbCreds['port']}
Creds   = {dbCreds['username']}/{dbCreds['password']}

""")
