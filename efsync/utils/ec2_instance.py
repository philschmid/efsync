import boto3
from efsync.utils.ec2_waiter import wait_for_ec2


def create_ec2_instance(bt3=None, security_group='', key_name='', subnet_Id=''):
    try:
        ec2 = bt3.resource('ec2')
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
            SecurityGroupIds=[
                security_group,
                'sg-5018d428'
            ],
            SubnetId=subnet_Id,
            KeyName=key_name
        )
        wait_for_ec2(instance_id=instance[0].id, wait_type='start')
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
        wait_for_ec2(instance_id=instance_id, wait_type='terminate')
        return True
    except Exception as e:
        err = repr(e)
        print(err)
        raise(e)
