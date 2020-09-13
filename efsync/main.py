import os
import boto3
import sys
import yaml
from efsync.utils import create_dir, create_secruity_group, create_ssh_key, get_security_group_id, create_ec2_instance, mount_efs, terminate_ec2_instance, delete_ssh_key, delete_secruity_group, install_pip_on_ec2, copy_files_to_ec2
from efsync.logger import get_logger
import time
import argparse
logger = get_logger()


def load_args_from_yaml(yaml_file):
    logger.info('loading yaml configuration')
    with open(yaml_file, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as e:
            raise(e)
            logger.error(
                f'could load {yaml_file} either it doesn´t exist or there are mistakes')


def get_boto3_client(args):
    try:
        logger.info('create boto3 session')
        args['bt3'] = boto3.session.Session(
            profile_name=args['aws_profile'], region_name=args['aws_region'])
        return args
    except Exception as e:
        raise(e)


def get_args(config_file):
    try:
        args = load_args_from_yaml(config_file)
        args = get_boto3_client(args)
        return args
    except Exception as e:
        raise(e)


def efsync(input_args):
    try:
        start = time.time()
        logger.info('starting....')
        #
        # parse args
        #
        # efsync -cf efsync.yaml
        if isinstance(input_args, dict) and 'config_file' in input_args and os.path.isfile(input_args['config_file']):
            logger.info(f'loading config from {input_args["config_file"]}')
            args = get_args(input_args['config_file'])
            logger.info('loaded config')
        # from efsync import efsync
        # efsync('efsync.yaml')
        elif isinstance(input_args, str):
            logger.info(f'loading config from {input_args}')
            args = get_args(input_args)
            logger.info('loaded config')
        # efsync ........
        else:
            logger.info(f'using CLI parameters')
            args = get_boto3_client(input_args)
        #
        # create .efsync directory
        #
        logger.info('create .efsync directory')
        create_dir()
        logger.info('created directory')

        #
        # creates security_group
        #
        logger.info(f"creating security group")
        try:
            security_id = create_secruity_group(args['bt3'])
            logger.info(f'created security group {security_id}')
        except Exception as e:
            logger.info(f"security group creation failed, already exists")
            security_id = get_security_group_id(args['bt3'])
            logger.info(f'using existing security group {security_id}')
        #
        # creates ssh key for scp and ssh in .efsync
        #
        logger.info('creating ssh key for scp and ssh in .efsync')
        try:
            create_ssh_key(args['bt3'], args['ec2_key_name'])
        except Exception as e:
            logger.info(
                f"recreating ssh key {args['ec2_key_name']}")
            delete_ssh_key(args['bt3'], args['ec2_key_name'])
            create_ssh_key(args['bt3'], args['ec2_key_name'])
        logger.info('created ssh key for scp and ssh in .efsync')
        #
        # starts ec2 instance in vpc with security group and ssh key
        #
        logger.info(
            f"starting ec2 instance with security group {security_id} and subnet_Id {args['subnet_Id']}")
        instance_id = create_ec2_instance(
            bt3=args['bt3'], security_group=security_id, key_name=args['ec2_key_name'], subnet_Id=args['subnet_Id'])
        logger.info('started ec2 instance')
        #
        # mounts efs file system with instance id
        #
        logger.info(f'mount efs file system with instance {instance_id}')
        logger.info(f'sleeping 30 seconds.... wait ec2 is up completely')
        time.sleep(30)
        mount_efs(bt3=args['bt3'], instance_id=instance_id, efs_filesystem_id=args['efs_filesystem_id'],
                  clean_efs=args['clean_efs'], ec2_key_name=args['ec2_key_name'], logger=logger)
        logger.info('mounted efs')
        #
        # install pip requirements
        #
        if 'requirements' in args and 'efs_pip_dir' in args:
            logger.info(f"installing pip packages to {args['efs_pip_dir']}")
            install_pip_on_ec2(
                python_version=args['python_version'], pip_dir=args['efs_pip_dir'])
            logger.info('installed pip packages')
        #
        # copy all files with scp from local directory to ec2 mounted efs
        #
        #
        # if 'requirements' in args and 'efs_pip_dir' in args:
        #     logger.info('coping pip packages with scp to ec2 instance')
        #     copy_files_to_ec2(bt3=args['bt3'], instance_id=instance_id, mv_dir=f".efsync/{args['efs_pip_dir']}", ec2_key_name=args['ec2_key_name']
        #                       )
        #     logger.info('copied pip packages')
        if 'file_dir' in args:
            logger.info(f"coping files from {args['file_dir']} to ec2")
            copy_files_to_ec2(bt3=args['bt3'], instance_id=instance_id, mv_dir=args['file_dir'], ec2_key_name=args['ec2_key_name']
                              )
            logger.info(f"copied files from {args['file_dir']}")
        #
        # stops ec2 instance after file transfer
        #
        logger.info(f"stopping ec2 instance with instance id {instance_id}")
        terminate_ec2_instance(bt3=args['bt3'], instance_id=instance_id)
        logger.info("ec2 instance stopped")
        #
        # deletes ssh key on aws
        #
        logger.info('deleting ssh key')
        delete_ssh_key(args['bt3'], args['ec2_key_name'])
        logger.info('key deleted')
        #
        # deletes secruity group on ec2
        #
        logger.info('deleting security group')
        delete_secruity_group(args['bt3'], security_id)
        logger.info('security group deleted')

        # deletes local directory #optional
        # delete_dir()
        logger.info(
            f'#################### finished after {round(time.time()-start,2)/60} minutes ####################')

    except Exception as e:
        err = repr(e)
        raise(err)
