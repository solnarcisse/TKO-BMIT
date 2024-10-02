import boto3
import schedule
import operator import itemgetter

ec2_client = boto3.client('ec2', region_name='us-east-1')
ec2_resource = boto3.client('ec2', region_name='us-east-1')

snapshots = ec2_client.describe_snapshots(
        OwnerIds=['self'],
        Filters=[
            {
                'Name': 'tag:volume-id',
                'Values': [volume['VolumeId']]
            }
        ]
    )


latest_snapshot = sorted(snapshots['Snapshots'], key=itemgetter('StartTime'), reverse=True)[0]
print(latest_snapshot['StartTime'])

new_volume = ec2_client.create_volume(
    SnapshotId=latest_snapshot['SnapshotId'],
    AvailabilityZone='us-east-1a',
    TagSpecification=[
        {
            'ResourceType': 'volume',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'Prod'
                }
            ]
        }
        ],
    VolumeType='gp2'
)

while True:
    vol = ec2_resource.Volume(new_volume['VolumeId'])
    if vol.state == 'available':
        ec2_resource.Instance(instance_id).attach_volume(
        Device='/dev/xvdb',
        InstanceId=instance_id,
        VolumeId=new_volume['VolumeId']
    )
        break
