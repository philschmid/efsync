import boto3
from efsync.utils.ec2.ec2_waiter import wait_for_ec2
from efsync.utils.ec2.create_user_data import create_user_data
from efsync.utils.security_group.ec2_security_group import get_security_group_id
from efsync.utils.iam_profile.iam_profile import create_iam_profile, delete_iam_profile
from efsync.utils.ec2.custom_waiter import custom_waiter

import time


def create_ec2_instance(config: dict = None):
    try:
        ec2 = config['bt3'].resource('ec2')
        instance_profile = create_iam_profile(config)
        user_data = create_user_data(config)
        # was to fast for aws after creation
        time.sleep(10)
        instance = ec2.create_instances(
            BlockDeviceMappings=[
                {
                    'DeviceName': '/dev/sdh',
                    'VirtualName': 'ephemeral0',
                    'Ebs': {
                        'DeleteOnTermination': True,
                        'VolumeSize': 10,
                        'VolumeType': 'gp2',
                        'Encrypted': False,
                    },
                },
            ],
            ImageId='ami-00edb93a4d68784e3',
            MinCount=1,
            MaxCount=1,
            InstanceType='t2.micro',
            UserData=user_data,
            SecurityGroupIds=[
                config['security_group'],
                config['default_sec_id'],

            ],
            SubnetId=config['subnet_Id'],
            KeyName=config['key']['name'],
            IamInstanceProfile={'Arn': instance_profile['Arn']})
        # waits till it running
        wait_for_ec2(bt3=config['bt3'],
                     instance_id=instance[0].id, wait_type='start')
        # waits till user_data == 'True' tag is set
        custom_waiter(config, instance[0].id)
        return instance[0].id
    except Exception as e:
        print(repr(e))
        raise(e)


def terminate_ec2_instance(bt3=None, instance_id=''):
    try:
        ec2 = bt3.resource('ec2')
        instance = ec2.Instance(instance_id)
        # ec2.instances.filter(InstanceIds=[instance_id]).terminate()
        instance.terminate()
        wait_for_ec2(bt3=bt3, instance_id=instance_id, wait_type='terminate')
        return True
    except Exception as e:
        err = repr(e)
        print(err)
        raise(e)
