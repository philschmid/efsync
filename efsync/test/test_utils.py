import pytest
from pytest import assume

import boto3
from efsync.utils.dir import create_dir, delete_dir
from efsync.utils.pip_install_local import pip_install_requirements
from efsync.utils.ec2_install_pip import install_pip_on_ec2, read_requirements_from_file
from efsync.utils.ssh_key import create_ssh_key, delete_ssh_key
from efsync.utils.ec2_security_group import create_secruity_group, delete_secruity_group, get_security_group_id
from efsync.utils.ec2_instance import create_ec2_instance, terminate_ec2_instance
from efsync.utils.ec2_mount_efs import mount_efs
from efsync.utils.scp_to_ec2 import copy_files_to_ec2

profile = 'schueler'
region = 'eu-central-1'
key_name = 'unit-tests-12312'
subnet_Id = 'subnet-17f97a7d'
efs_filesystem_id = 'fs-2226b27a'
test_dor = 'efsync/test/data'


def test_dir():
    res = create_dir()
    with assume:
        assert res == True
    res = delete_dir()
    with assume:
        assert res == True

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
    res = delete_secruity_group(bt3, res)
    with assume:
        assert res == True


def test_ssh_key():
    bt3 = boto3.session.Session(
        profile_name=profile, region_name=region)
    create_dir()
    res = create_ssh_key(bt3, key_name)
    with assume:
        assert res == True
    res = delete_ssh_key(bt3, key_name)
    delete_dir()
    with assume:
        assert res == True


def test_get_default_security_group_id():
    bt3 = boto3.session.Session(
        profile_name=profile, region_name=region)
    res = get_security_group_id(bt3, 'default')
    assert len(res) > 1


def test_ec2_instance():
    bt3 = boto3.session.Session(
        profile_name=profile, region_name=region)
    ins_id, security_id = helper_create_ec2_instance(bt3)
    with assume:
        assert len(ins_id) > 0 and len(security_id) > 0
    res = helper_del_ec2_instance(bt3=bt3, ins_id=ins_id, sec_id=security_id)
    with assume:
        assert res == True


def helper_create_ec2_instance(bt3):
    # pre
    res = create_dir()
    with assume:
        assert res == True

    security_id = create_secruity_group(bt3)
    with assume:
        assert len(security_id) > 0
    res = create_ssh_key(bt3, key_name)
    with assume:
        assert res == True
    ins_id = create_ec2_instance(bt3=bt3, security_group=security_id,
                                 subnet_Id=subnet_Id, key_name=key_name)
    with assume:
        assert len(ins_id) > 0
    return ins_id, security_id


def helper_del_ec2_instance(bt3, ins_id, sec_id):
    # post
    res = terminate_ec2_instance(bt3=bt3, instance_id=ins_id)
    with assume:
        assert res == True
    res = delete_ssh_key(bt3, key_name)
    with assume:
        assert res == True
    res = delete_secruity_group(bt3, sec_id)
    with assume:
        assert res == True
    return True


def test_mount_efs():
    bt3 = boto3.session.Session(
        profile_name=profile, region_name=region)
    # pre
    ins_id = helper_create_ec2_instance(bt3)
    with assume:
        assert len(ins_id) > 0
    # test
    res = mount_efs(bt3=bt3, instance_id=ins_id, efs_filesystem_id=efs_filesystem_id,
                    clean_efs=True, ec2_key_name=key_name)
    with assume:
        assert res == True
    # after
    res = helper_del_ec2_instance(bt3=bt3, instance_id=ins_id)
    with assume:
        assert res == True


def test_read_requirements_from_file():
    file_path = 'requirements.txt'
    res = read_requirements_from_file(file_path)
    assert isinstance(res, str)


def test_scp_to_ec2_efs():
    bt3 = boto3.session.Session(
        profile_name=profile, region_name=region)
    # pre
    ins_id = helper_create_ec2_instance(bt3)
    with assume:
        assert len(ins_id) > 0
    # test
    res = copy_files_to_ec2(bt3=bt3, instance_id=ins_id,
                            mv_dir=test_file, ec2_key_name=key_name)
    with assume:
        assert res == True
    # after
    res = helper_del_ec2_instance(bt3=bt3, instance_id=ins_id)
    with assume:
        assert res == True


def test_ec2_pip_install():
    bt3 = boto3.session.Session(
        profile_name=profile, region_name=region)
    # pre
    ins_id = helper_create_ec2_instance(bt3)
    with assume:
        assert len(ins_id) > 0
    # test
    res = install_pip_on_ec2(bt3=bt3, instance_id=ins_id, python_version="3.8",
                             pip_dir='lib', ec2_key_name=key_name, file='requirements.txt')
    with assume:
        assert res == True
    # after
    res = helper_del_ec2_instance(bt3=bt3, instance_id=ins_id)
    with assume:
        assert res == True
