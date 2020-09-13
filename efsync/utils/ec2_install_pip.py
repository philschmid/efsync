from efsync.utils.helper.createSSHClient import createSSHClient
import paramiko
import boto3
# https: // serverfault.com/questions/836198/how-to-install-docker-on-aws-ec2-instance-with-ami-ce-ee-update
# install everythin directly into efs instead of copying it


def read_requirements_from_file(file_path):
    try:
        # read all requirements from file and remove \n
        install_list = open(file_path, 'r').read().splitlines()
        # removes empty lines and comments
        install_requires = [
            str(requirement)
            for requirement
            in install_list if not requirement.startswith('#') and len(requirement) > 0]
        return ' '.join(install_requires)
    except Exception as e:
        print(e)
        raise(e)


def install_pip_on_ec2(bt3=None, instance_id=None, python_version=None, pip_dir=None, ec2_key_name=None, logger=None, file=None):
    try:
        # read requirements into file_string
        requirements_string = read_requirements_from_file(file)
        # get boto3 client
        client = bt3.client('ec2')
        response = client.describe_instances(InstanceIds=[instance_id])
        # get public dns
        public_dns_name = response['Reservations'][0]['Instances'][0]['NetworkInterfaces'][0]['Association']['PublicDnsName']
        # connect ssh
        ssh = createSSHClient(
            public_dns_name=public_dns_name, ec2_key_name=ec2_key_name)
        # update packages
        stdin, stdout, stderr = ssh.exec_command(
            'sudo yum update -y')
        stdin.flush()
        logger.info(stdout.read().decode('utf-8'))
        # install docker on ec2
        stdin, stdout, stderr = ssh.exec_command(
            'sudo yum install docker -y')
        stdin.flush()
        logger.info(stdout.read().decode('utf-8'))
        # start docker service
        stdin, stdout, stderr = ssh.exec_command(
            f'sudo service docker start')
        stdin.flush()
        logger.info(stdout.read().decode('utf-8'))
        # install pip packages to directory
        stdin, stdout, stderr = ssh.exec_command(
            f'sudo docker run -v "$PWD":/var/task lambci/lambda:build-python{python_version} pip3 --no-cache-dir install -t efs/{pip_dir} {requirements_string}')
        stdin.flush()
        logger.info(stdout.read().decode('utf-8'))
    except Exception as e:
        print(e)
        raise(e)
    finally:
      # close ssh connection
        ssh.close()
        return True
