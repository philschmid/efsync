import boto3


def create_secruity_group(bt3=None):
    try:
        ec2 = bt3.client('ec2')
        sec_group = ec2.create_security_group(
            GroupName='efsync-group', Description='efsync-group sec group')
        ec2.authorize_security_group_ingress(GroupId=sec_group['GroupId'],
                                             IpProtocol="tcp",
                                             CidrIp="0.0.0.0/0",
                                             FromPort=22, ToPort=22)
        return sec_group['GroupId']
    except Exception as e:
        try:
            return get_security_group_id(bt3)
        except Exception as e:
            print(repr(e))
            raise(e)


def get_security_group_id(bt3=None, group_name='efsync-group'):
    try:
        ec2 = bt3.client('ec2')
        response = ec2.describe_security_groups(
            Filters=[
                dict(Name='group-name', Values=[group_name])
            ]
        )
        group_id = response['SecurityGroups'][0]['GroupId']
        return group_id
    except Exception as e:
        raise(e)


def delete_secruity_group(bt3=None, group_id=''):
    try:
        ec2 = bt3.client('ec2')
        if len(group_id) > 0:
            sec_group = ec2.delete_security_group(GroupId=group_id,
                                                  GroupName='efsync-group')
        else:
            sec_group = ec2.delete_security_group(GroupName='efsync-group')
        return True
    except Exception as e:
        print(repr(e))
        raise(e)
