import boto3
import paramiko
from efsync.utils.helper.createSSHClient import createSSHClient


def write_to_log(file_string):
    try:
        with open(f'.efsync/logs', 'w') as out_file:
            for entry in file_string:
                out_file.write(entry.decode("utf-8"))
                out_file.write('\n')
    except Exception as e:
        raise(e)


def mount_efs(bt3, instance_id, efs_filesystem_id='fs-2226b27a', clean_efs=True):
    try:
        client = bt3.client('ec2')
        response = client.describe_instances(InstanceIds=[instance_id])
        # get public dns
        public_dns_name = response['Reservations'][0]['Instances'][0]['NetworkInterfaces'][0]['Association']['PublicDnsName']
        # connect ssh
        ssh = createSSHClient(public_dns_name=public_dns_name)
        # install efs mount helper
        stdin, stdout, stderr = ssh.exec_command(
            'sudo yum install -y amazon-efs-utils')
        stdin.flush()
        data = stdout.read().splitlines()
        # @TODO: Add logger
        write_to_log(data)
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
        write_to_log(data)
        # chown for scp
        stdin, stdout, stderr = ssh.exec_command(
            'sudo chown -R ec2-user:ec2-user efs')
        stdin.flush()
        data = stdout.read().splitlines()
        # @TODO: Add logger
        write_to_log(data)
        # clean efs if wanted
        if(clean_efs):
            stdin, stdout, stderr = ssh.exec_command(
                ' rm -r efs/*')
            stdin.flush()
            data = stdout.read().splitlines()
            # @TODO: Add logger
            write_to_log(data)

    except Exception as e:
        print(e)
        raise(e)
    finally:
      # close ssh connection
        ssh.close()
        return True
    # try:
    #     ssm_client = bt3.client('ssm')
    #     resp = ssm_client.send_command(
    #         DocumentName="AWS-RunShellScript",  # One of AWS' preconfigured documents
    #         Parameters={'commands': ['sudo yum install -y amazon-efs-utils',
    #                                  'sudo mkdir efs', 'sudo mount -t efs -o tls fs-2226b27a:/ efs']},
    #         InstanceIds=[instance_ids],
    #     )
    #     return resp
    # except Exception as e:
    #     err = repr(e)
    #     raise(e)
