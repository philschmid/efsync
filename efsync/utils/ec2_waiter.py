import boto3


def wait_for_ec2(bt3=None, instance_id='', wait_type=''):
    ec2_client = bt3.client('ec2')
    try:
        if wait_type == 'terminate':
            waiter = ec2_client.get_waiter('instance_terminated')
        elif wait_type == 'start':
            waiter = ec2_client.get_waiter('instance_running')
        waiter.wait(InstanceIds=[instance_id])
        return True
    except Exception as e:
        err = repr(e)
        raise(e)
