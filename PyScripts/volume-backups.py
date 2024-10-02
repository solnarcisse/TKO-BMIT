import boto3
import time
import schedule

ec2_client = boto3.client('ec2', region_name='us-east-1')

def create_volume_snapshots():
    volumes = ec2_client.describe_volumes(
        Filters=[
            {
                'Name': 'tag:Name',
                'Values': ['Prod']
            }
        ]
    )
    for volume in volumes['Volumes']:
        new_snapshot = ec2_client.create_snapshot(
            VolumeId=volume['VolumeId'],
            Description='Snapshot created by XXXXXX function'
        )
        print (new_snapshot)
    
schedule.every().day.do(create_volume_snapshots)

while True:
    schedule.run_pending()
    time.sleep(1)