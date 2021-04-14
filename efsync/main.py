import os
import boto3
import sys
import time
from efsync.utils.ssh.ssh_key import create_ssh_key, delete_ssh_key
from efsync.utils.security_group.ec2_security_group import create_secruity_group, delete_secruity_group, get_security_group_id
from efsync.utils.ec2.ec2_main import create_ec2_instance, terminate_ec2_instance
from efsync.utils.iam_profile.iam_profile import delete_iam_profile
from efsync.utils.ssh.scp_to_ec2 import copy_files_to_ec2

from efsync.utils.config.load_config import load_config

from efsync.logger import get_logger
import argparse


logger = get_logger()

def efsync(input_args):
    try:
        start = time.time()
        logger.info('starting....')
        #
        # load config 
        #
        logger.info('loading config')
        config = load_config(input_args)
        #
        # creates security_group
        #
        logger.info(f"creating security group")
        try:
            config['security_group'] = create_secruity_group(config['bt3'])
        except Exception as e:
            raise(e)
        # 
        # get default security group
        #
        logger.info(f"loading default security group")
        try:
            config['default_sec_id'] = get_security_group_id(config['bt3'], 'default')
        except Exception as e:
            raise(e)
        
        #
        # creating ssh key for scp in memory
        #
        logger.info('creating ssh key for scp in memory')
        try:
            config['key'] = create_ssh_key(config['bt3'],  config['ec2_key_name'])
        except Exception as e:
            raise(e)
            
        #
        # starts ec2 instance in vpc with security group and ssh key
        #
        logger.info(
            f"starting ec2 instance with security group {config['security_group']} and subnet_Id {config['subnet_Id']}")
        config['instance_id'] = create_ec2_instance(config)
        
        #
        # copy all files with scp from local directory to ec2 mounted efs
        #
        #
        if 'file_dir' in config and 'file_dir_on_ec2' in config:
            logger.info(f"coping files from {config['file_dir']} to /home/ec2-user/efs/{config['file_dir_on_ec2']} ")
            copy_files_to_ec2(config)        
        #
        # stopping and deleting every ressource
        #
        # ec2
        logger.info(f"stopping ec2 instance with instance id {config['instance_id']}")
        terminate_ec2_instance(bt3=config['bt3'], instance_id=config['instance_id'])
        # iam profile
        logger.info(f"deleting iam profile")
        delete_iam_profile(config)
         # ssh key
        logger.info(f"deleting ssh key")
        delete_ssh_key(config['bt3'], config['key']['name'])
        # security group
        logger.info(f"deleting security group")
        delete_secruity_group(config['bt3'], config['security_group'])

        logger.info(
            f'#################### finished after {round(time.time()-start,2)/60} minutes ####################')
        return True
    except Exception as e:
        err = repr(e)
        logger.error(err)
        try:
            if 'instance_id' in config:
                terminate_ec2_instance(bt3=config['bt3'], instance_id=config['instance_id'])
            delete_iam_profile(config)
            delete_ssh_key(config['bt3'], config['key']['name'])
            delete_secruity_group(config['bt3'], config['security_group'])
        except Exception as e:
            raise(e)
        raise(err)
