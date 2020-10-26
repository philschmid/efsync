import pytest
from pytest import assume

import boto3
# from efsync.utils.dir import create_dir, delete_dir
# from efsync.utils.pip_install_local import pip_install_requirements
# from efsync.utils.ec2_install_pip import install_pip_on_ec2, read_requirements_from_file
from efsync.utils.ssh.ssh_key import create_ssh_key, delete_ssh_key
from efsync.utils.security_group.ec2_security_group import create_secruity_group, delete_secruity_group, get_security_group_id
from efsync.utils.ec2.ec2_main import create_ec2_instance, terminate_ec2_instance
from efsync.utils.iam_profile.iam_profile import create_iam_profile, delete_iam_profile
from efsync.utils.efs.describe_efs import describe_file_systems
# from efsync.utils.ec2_mount_efs import mount_efs
from efsync.utils.ssh.scp_to_ec2 import copy_files_to_ec2
from efsync.utils.config.get_boto3_client import get_boto3_client
from efsync.utils.config.load_args_from_yaml import load_args_from_yaml
from efsync.utils.config.load_config import load_config
from efsync.utils.config.validate_config import validate_config
from efsync.utils.config.read_requirements_from_file import read_requirements_from_file
from efsync.utils.ec2.create_user_data import create_user_data
from efsync.utils.ec2.custom_waiter import custom_waiter


from efsync.logger import get_logger
logger = get_logger()


profile = 'schueler'
region = 'eu-central-1'
key_name = 'unit-tests-fgdfg'
subnet_Id = 'subnet-17f97a7d'
efs_filesystem_id = 'fs-2226b27a'
test_file_dir = 'efsync/test/data'


#! not used anymore
# def test_dir():
#     res = create_dir()
#     with assume:
#         assert res == True
#     res = delete_dir()
#     with assume:
#         assert res == True

# def test_pip_install():
#     # create_dir()
#     res = pip_install_requirements()
#     # delete_dir()
#     assert res == True


def test_ec2_sec_group():
    bt3 = boto3.session.Session(
        profile_name=profile, region_name=region)
    res = create_secruity_group(bt3)
    with assume:
        assert len(res) > 0
    get_id = get_security_group_id(bt3)
    with assume:
        assert get_id == res
    res = delete_secruity_group(bt3, get_id)
    with assume:
        assert res == True


def test_ssh_key():
    bt3 = boto3.session.Session(
        profile_name=profile, region_name=region)
    res = create_ssh_key(bt3, key_name)
    assert '-----END RSA PRIVATE KEY-----' in res
    res = delete_ssh_key(bt3, key_name)
    assert res == True


def test_get_default_security_group_id():
    bt3 = boto3.session.Session(
        profile_name=profile, region_name=region)
    res = get_security_group_id(bt3, 'default')
    assert len(res) > 1


#! not used anymore -> mounting in user_data
# def test_mount_efs():
#     bt3 = boto3.session.Session(
#         profile_name=profile, region_name=region)
#     # pre
#     ins_id, security_id = helper_create_ec2_instance(bt3)
#     with assume:
#         assert len(ins_id) > 0 and len(security_id) > 0
#     # test
#     res = mount_efs(bt3=bt3, instance_id=ins_id, efs_filesystem_id=efs_filesystem_id,
#                     clean_efs=False, ec2_key_name=key_name, logger=logger)
#     with assume:
#         assert res == True
#     # after
#     res = helper_del_ec2_instance(bt3=bt3, ins_id=ins_id, sec_id=security_id)
#     with assume:
#         assert res == True


def test_ec2_instance():
    args = 'efsync/test/efsync.yaml'
    config = load_config(args)
    security_id = create_secruity_group(config['bt3'])
    config['security_group'] = security_id
    assert len(security_id) > 0
    config['default_sec_id'] = get_security_group_id(config['bt3'], 'default')
    config['key'] = create_ssh_key(config['bt3'], key_name)
    # start ec2
    ins_id = create_ec2_instance(config)
    config['instance_id'] = ins_id
    assert len(ins_id) > 0
    res = terminate_ec2_instance(
        bt3=config['bt3'], instance_id=config['instance_id'])
    assert res == True
    res = delete_iam_profile(config)
    assert res == True
    res = delete_ssh_key(config['bt3'], config['key']['name'])
    assert res == True
    res = delete_secruity_group(config['bt3'], config['security_group'])
    assert res == True


def test_scp_to_ec2_efs():
    bt3 = boto3.session.Session(
        profile_name=profile, region_name=region)
    # # pre
    ins_id, security_id = helper_create_ec2_instance(bt3)
    with assume:
        assert len(ins_id) > 0 and len(security_id) > 0
    # mount
    # res = mount_efs(bt3=bt3, instance_id=ins_id, efs_filesystem_id=efs_filesystem_id,
    #                 clean_efs=False, ec2_key_name=key_name, logger=logger)
    # with assume:
    #     assert res == True
    # test
    res = copy_files_to_ec2(bt3=bt3, instance_id=ins_id, ec2_dir='files',
                            mv_dir=test_file_dir, ec2_key_name=key_name)
    with assume:
        assert res == True
    # after
    res = helper_del_ec2_instance(
        bt3=bt3, ins_id=ins_id, sec_id=security_id)
    with assume:
        assert res == True

#! not used anymore -> install in user_data
# def test_ec2_pip_install():
#     bt3 = boto3.session.Session(
#         profile_name=profile, region_name=region)
#     # # pre
#     ins_id, security_id = helper_create_ec2_instance(bt3)
#     with assume:
#         assert len(ins_id) > 0 and len(security_id) > 0

#     # test
#     res = install_pip_on_ec2(bt3=bt3, instance_id=ins_id, python_version="3.8",
#                              pip_dir='lib', ec2_key_name=key_name, file='requirements.txt', logger=logger)
#     with assume:
#         assert res == True
#     # after
#     res = helper_del_ec2_instance(bt3=bt3, ins_id=ins_id, sec_id=security_id)
#     with assume:
#         assert res == True


def test_create_iam_profile():
    args = 'efsync/test/efsync.yaml'
    config = load_config(args)
    res = create_iam_profile(config)
    assert isinstance(res, dict)


def test_delete_iam_profile():
    args = 'efsync/test/efsync.yaml'
    config = load_config(args)

    res = delete_iam_profile(config)
    assert res == True


def test_describe_file_systems():
    bt3 = boto3.session.Session(
        profile_name=profile, region_name=region)
    res = describe_file_systems(bt3=bt3, file_system_id=efs_filesystem_id)
    assert res == True


def test_get_boto3_client():
    args = {'aws_profile': profile, 'aws_region': region}
    res = get_boto3_client(args)
    assert isinstance(res, dict)


def test_load_args_from_yaml():
    res = load_args_from_yaml('efsync/test/efsync.yaml')
    assert isinstance(res, dict)


def test_load_config():
    args = {'config_file': 'efsync/test/efsync.yaml'}
    res = load_config(args)
    assert isinstance(res, dict)

    args = 'efsync/test/efsync.yaml'
    res = load_config(args)
    assert isinstance(res, dict)

    args = {'aws_profile': profile, 'aws_region': region}
    res = load_config(args)
    assert isinstance(res, dict)


def test_read_requirements_from_file():
    res = read_requirements_from_file('efsync/test/requirements.txt')
    assert isinstance(res, str)


def test_create_user_data():
    # test clean efs
    config = {'aws_profile': 'schueler-vz', 'aws_region': 'eu-central-1', 'efs_filesystem_id': '123',
              'clean_efs': 'all',
              }
    res = create_user_data(config)
    assert 'sudo rm -rf efs/*' in res
    # test pip install
    config = {'aws_profile': 'schueler-vz', 'aws_region': 'eu-central-1',  'efs_filesystem_id': efs_filesystem_id,
              'efs_pip_dir': 'lib', 'python_version': 3.8, 'requirements': 'efsync/test/requirements.txt',
              'clean_efs': 'pip',
              }
    res = create_user_data(config)
    assert f'{config["efs_pip_dir"]}' in res
    assert f'sudo rm -rf efs/{config["efs_pip_dir"]}/*' in res
    # test s3
    config = {'aws_profile': 'schueler-vz', 'aws_region': 'eu-central-1',  'efs_filesystem_id': efs_filesystem_id,
              'file_dir_on_ec2': 'ml', 's3_keyprefix': 'model/bert', 's3_bucket': 'mybucket',
              'clean_efs': 'file',
              }
    res = create_user_data(config)
    assert f'{config["s3_bucket"]}' in res
    assert f'sudo rm -rf efs/{config["file_dir_on_ec2"]}/*' in res
    # test all
    config = {'aws_profile': 'schueler-vz', 'aws_region': 'eu-central-1',  'efs_filesystem_id': efs_filesystem_id,
              'efs_pip_dir': 'lib', 'python_version': 3.8, 'requirements': 'efsync/test/requirements.txt',
              'file_dir_on_ec2': 'ml', 's3_keyprefix': 'model/bert', 's3_bucket': 'mybucket',
              'clean_efs': 'all',
              }
    res = create_user_data(config)
    assert f'{config["s3_bucket"]}' in res
    assert f'{config["efs_pip_dir"]}' in res
    assert f'{config["s3_bucket"]}' in res
    assert 'sudo rm -rf efs/*' in res
    f = open("user_data", "a")
    f.write(res)
    f.close()


def test_custom_waiter():
    args = 'efsync/test/efsync.yaml'
    config = load_config(args)
    res = custom_waiter(config, 'i-0924fcb5b23576a9f')


def test_validate_config():
    # test all
    config = {'aws_profile': 'schueler-vz', 'aws_region': 'eu-central-1',  'efs_filesystem_id': 'as','subnet_Id':'123',
              'efs_pip_dir': 'lib', 'python_version': 3.8, 'requirements': 'efsync/test/requirements.txt',
              'file_dir_on_ec2': 'ml', 's3_keyprefix': 'model/bert', 's3_bucket': 'mybucket',"ec2_key_name":'123',
              'clean_efs': 'all',
              }    
    res = validate_config(config)
    assert res == True
    # test s3
    config = {'aws_profile': 'schueler-vz', 'aws_region': 'eu-central-1',  'efs_filesystem_id': efs_filesystem_id,'subnet_Id':'123',
              'file_dir_on_ec2': 'ml', 's3_keyprefix': 'model/bert', 's3_bucket': 'mybucket',"ec2_key_name":'123',
              'clean_efs': 'file',
              }
    res = validate_config(config)
    assert res == True

    # test pip install
    config = {'aws_profile': 'schueler-vz', 'aws_region': 'eu-central-1',  'efs_filesystem_id': efs_filesystem_id,'subnet_Id':'123',
              'efs_pip_dir': 'lib', 'python_version': 3.8, 'requirements': 'efsync/test/requirements.txt',"ec2_key_name":'123',
              'clean_efs': 'pip',
              }
    res = validate_config(config)
    assert res == True
    # test scp
    config = {'aws_profile': 'schueler-vz', 'aws_region': 'eu-central-1',  'efs_filesystem_id': efs_filesystem_id,'subnet_Id':'123',
              'file_dir_on_ec2': 'ml', 'file_dir': 'model/bert',"ec2_key_name":'123',
              'clean_efs': 'file',
              }
    res = validate_config(config)
    assert res == True