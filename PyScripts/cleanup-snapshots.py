import boto3
import schedule
import operator import itemgetter

ec2_client = boto3.client('ec2', region_name='us-east-1')

def cleanup_snapshots():

    volumes = ec2_client.describe_volumes(
            Filters=[
                {
                    'Name': 'tag:Name',
                    'Values': ['Prod']
                }
            ]
        )

    for volume in volumes['Volumes']:
        #print(volume['VolumeId'])
        snapshots = ec2_client.describe_snapshots(
            OwnerIds=['self'],
            Filters=[
                {
                    'Name': 'tag:volume-id',
                    'Values': [volume['VolumeId']]
                }
            ]
        )
        
        
        

        sorted_by_date = sorted(snapshots['Snapshots'], key=itemgetter('StartTime'), reverse=True)

        ## for snap in snapshots['Snapshots']:
            ##print(snap['StartTime'])
        ##print('------------------')
        ##print('------------------')

        ##for snap in sorted_by_date:
            ##print(snap['StartTime'])
            
        for snap in sorted_by_date [2:]:
            ##print(snap['SnapshotId'])
            ##print(snap['StartTime'])
            
            ec2_client.delete_snapshot(
                SnapshotId=snap['SnapshotId']
            )
            print(response)

schedule.every().day.do(cleanup_snapshots)

while True:
        schedule.run_pending()
        time.sleep(1)