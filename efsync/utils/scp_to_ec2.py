import paramiko
from scp import SCPClient
from efsync.utils.helper.createSSHClient import createSSHClient
import boto3


def copy_files_to_ec2(bt3=None, instance_id='', mv_dir='', ec2_dir='/home/ec2-user/efs', ec2_key_name=None):
    try:
        client = bt3.client('ec2')
        response = client.describe_instances(InstanceIds=[instance_id])
        # get public dns
        public_dns_name = response['Reservations'][0]['Instances'][0]['NetworkInterfaces'][0]['Association']['PublicDnsName']
        # connect ssh
        ssh = createSSHClient(
            public_dns_name=public_dns_name, ec2_key_name=ec2_key_name)
        scp = SCPClient(ssh.get_transport())
        # Uploading the 'test' directory with its content in the
        # '/home/user/dump' remote directory
        scp.put(mv_dir, recursive=True, remote_path=ec2_dir)
    except Exception as e:
        logger.error(repr(e))
        raise(e)
    finally:
        scp.close()
        ssh.close()
        return True
