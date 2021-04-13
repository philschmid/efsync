import boto3

def get_vpc_id(bt3=None, subnet_id):
    try:
        ec2 = bt3.client('ec2')
        response = ec2.describe_subnets(
            Filters=[{
                'Name': 'subnet-id',
                'Values': [subnet_id]
            }]
        )
        vpc_id = response['Subnets'][0]['VpcId']
        return vpc_id
    except Exception as e:
        raise(e)