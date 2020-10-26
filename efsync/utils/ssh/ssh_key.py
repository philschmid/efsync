import boto3
from uuid import uuid4
import os

# key is now hold in memory
# def write_key_to_file(file_string=None, file_path='.', key_name=''):
#     try:
#         if os.path.isfile(f'{file_path}/{key_name}.pem'):
#             os.chmod(f'{file_path}/{key_name}.pem', 0o777)
#         with open(f'{file_path}/{key_name}.pem', 'w+') as out_file:
#             out_file.write(file_string)
#         os.chmod(f'{file_path}/{key_name}.pem', 0o400)
#     except Exception as e:
#         print(e)
#         raise(e)


def create_ssh_key(bt3=None, key_name=''):
    try:
        ec2 = bt3.client('ec2')
        response = ec2.create_key_pair(KeyName=key_name)
        return {'name': key_name, 'value': response['KeyMaterial']}
    except Exception as e:
        res = delete_ssh_key(bt3, key_name)
        if res:
            return create_ssh_key(bt3, key_name)
        else:
            raise(e)


def delete_ssh_key(bt3=None, key_name=''):
    try:
        ec2 = bt3.client('ec2')
        response = ec2.delete_key_pair(KeyName=key_name)
        return True
    except Exception as e:
        print(repr(e))
        raise(e)
