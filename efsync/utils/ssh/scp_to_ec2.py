import paramiko
from scp import SCPClient
from efsync.utils.ssh.createSSHClient import createSSHClient
import boto3


def copy_files_to_ec2(config):
    try:
        default_ec2_path = '/home/ec2-user/efs'
        client = config['bt3'].client('ec2')
        response = client.describe_instances(
            InstanceIds=[config['instance_id']])
        # get public dns
        public_dns_name = response['Reservations'][0]['Instances'][0]['NetworkInterfaces'][0]['Association']['PublicDnsName']
        # connect ssh
        ssh = createSSHClient(
            public_dns_name=public_dns_name, key=config['key'])
        scp = SCPClient(ssh.get_transport())
        # Uploading the 'test' directory with its content in the
        # '/home/user/dump' remote directory
        scp.put(config['file_dir'], recursive=True,
                remote_path=f"{default_ec2_path}/{config['file_dir_on_ec2']}")
    except Exception as e:
        logger.error(repr(e))
        raise(e)
    finally:
        scp.close()
        ssh.close()
        return True
