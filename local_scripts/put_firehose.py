import boto3
import json
from fake_web_events import Simulation

client = boto3.client("firehose")


def put_record(event):
    data = json.dumps(event) + "\n"
    response = client.put_record(
        DeliveryStreamName="firehose-develop-raw-delivery-stream",
        Record={"Data": data},
    )
    #print(event)

    return response


simulation = Simulation(user_pool_size=10, sessions_per_day=100)
events = simulation.run(duration_seconds=100)
for event in events:
    put_record(event)