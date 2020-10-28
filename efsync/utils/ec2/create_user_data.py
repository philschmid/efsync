
from efsync.utils.config.read_requirements_from_file import read_requirements_from_file


def create_user_data(config: dict = None):
    try:
        user_data = []
        if not 'efs_filesystem_id' in config:
            raise Exception('Missing efs_filesystem_id in config')
        user_data.append('#!/bin/bash')
        user_data.append('sudo yum update -y')
        user_data.append('sudo yum install -y amazon-efs-utils')
        user_data.append('sudo mkdir efs')
        user_data.append(
            f'sudo mount -t efs -o tls {config["efs_filesystem_id"]}:/ efs')
        user_data.append('sudo chown -R ec2-user:ec2-user efs')

        if 'clean_efs' in config and config['clean_efs'] == 'all':
            user_data.append('sudo rm -rf efs/*')

        if 'efs_pip_dir' in config and 'requirements' in config and 'python_version' in config:
            requirements_string = read_requirements_from_file(
                config['requirements'])
            if 'clean_efs' in config and config['clean_efs'] == 'pip':
                user_data.append(f'sudo rm -rf efs/{config["efs_pip_dir"]}/*')
            user_data.append('sudo yum install docker -y')
            user_data.append('sudo service docker start')
            user_data.append(
                f'sudo docker run -v "$PWD":/var/task lambci/lambda:build-python{config["python_version"]} pip3 --no-cache-dir install -t efs/{config["efs_pip_dir"]} {requirements_string}')

        if 's3_bucket' in config and 's3_keyprefix' in config and 'file_dir_on_ec2' in config:
            if 'clean_efs' in config and config['clean_efs'] == 'file':
                user_data.append(
                    f'sudo rm -rf efs/{config["file_dir_on_ec2"]}/*')
            user_data.append(
                f'aws s3 sync s3://{config["s3_bucket"]}/{config["s3_keyprefix"]} efs/{config["file_dir_on_ec2"]}')
        
        if 'file_dir_on_ec2' in config and 'file_dir' in config:
            if '/' in config["file_dir"]:
                additional_file_path = config["file_dir"].split("/")[-1]
            else: 
                 additional_file_path = config["file_dir"]
            
            user_data.append(
                    f'mkdir -p efs/{config["file_dir_on_ec2"]}/{additional_file_path}')
            
            user_data.append(
                    f'chmod 777  /efs/{config["file_dir_on_ec2"]}/{additional_file_path}')
        # add tag for user data finish script
        user_data.append(
            f"""aws ec2 create-tags --resources $(curl http://169.254.169.254/latest/meta-data/instance-id) --tags 'Key="user_data",Value=True' --region {config['aws_region']}""")

        return '\n'.join(user_data)
    except Exception as e:
        print(e)
        raise(e)
