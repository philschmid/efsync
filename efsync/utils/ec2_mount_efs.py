import boto3
import paramiko
from efsync.utils.helper.createSSHClient import createSSHClient



def mount_efs(bt3=None, instance_id=None, efs_filesystem_id=None, clean_efs=None,ec2_key_name=None):
    try:
        client = bt3.client('ec2')
        response = client.describe_instances(InstanceIds=[instance_id])
        # get public dns
        public_dns_name = response['Reservations'][0]['Instances'][0]['NetworkInterfaces'][0]['Association']['PublicDnsName']
        # connect ssh
        ssh = createSSHClient(public_dns_name=public_dns_name,ec2_key_name= ec2_key_name)
        # install efs mount helper
        stdin, stdout, stderr = ssh.exec_command(
            'sudo yum install -y amazon-efs-utils')
        stdin.flush()
        data = stdout.read().splitlines()
        # @TODO: Add logger
        # mount efs to ec2
        stdin, stdout, stderr = ssh.exec_command(
            'sudo mkdir efs')
        stdin, stdout, stderr = ssh.exec_command(
            f'sudo mount -t efs -o tls {efs_filesystem_id}:/ efs')
        stdin, stdout, stderr = ssh.exec_command(
            f' mount | grep /home/ec2-user/efs')
        stdin.flush()
        data = stdout.read().splitlines()
        # @TODO: Add logger
        # chown for scp
        stdin, stdout, stderr = ssh.exec_command(
            'sudo chown -R ec2-user:ec2-user efs')
        stdin.flush()
        data = stdout.read().splitlines()
        # @TODO: Add logger
        # clean efs if wanted
        if(clean_efs):
            stdin, stdout, stderr = ssh.exec_command(
                ' rm -r efs/*')
            stdin.flush()
            data = stdout.read().splitlines()

    except Exception as e:
        print(e)
        raise(e)
    finally:
      # close ssh connection
        ssh.close()
        return True
