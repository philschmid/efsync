import pytest
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


def test_create_dir():
    res = create_dir()
    assert res == True


def test_delete_dir():
    res = delete_dir()
    assert res == True


def test_pip_install():
    # create_dir()
    res = pip_install_requirements()
    # delete_dir()
    assert res == True


def test_create_ssh_key():
    create_dir()
    res = create_ssh_key()
    # delete_dir()
    assert res == True


def test_delete_ssh_key():
    # create_dir()
    res = delete_ssh_key()
    # delete_dir()
    assert res == True


def test_ec2_sec_group():
    res = create_secruity_group()
    assert isinstance(res, str)
    res = delete_secruity_group(group_id=res)
    assert res == True


def test_get_ec_security_group():
    bt3 = boto3.session.Session(profile_name=profile, region_name=region)
    res = get_security_group_id(bt3)
    print(res)
    assert len(res) > 0


def test_ec2_create_instance():
    create_dir()
    security_id = create_secruity_group()
    create_ssh_key()
    ins_id = create_ec2_instance(security_group=security_id,
                                 subnet_Id='subnet-17f97a7d')
    assert isinstance(ins_id, str)


def test_mount_efs():
    bt3 = boto3.session.Session(profile_name=profile, region_name=region)
    iid = 'i-0ce18ee13d9747027'
    res = mount_efs(bt3=bt3, instance_id=iid, efs_filesystem_id='fs-2226b27a',
                    clean_efs=True, ec2_key_name='efsync-asd913fjgq3')
    assert res == True


def test_read_requirements_from_file():
    file_path = 'requirements.txt'
    res = read_requirements_from_file(file_path)
    assert isinstance(res, str)


def test_scp_to_ec2_efs():
    bt3 = boto3.session.Session(profile_name=profile, region_name=region)
    iid = 'i-02e5ed4a7731b716f'
    res = copy_files_to_ec2(bt3, iid, '.efsync/lib')
    assert res == True


def test_ec2_delete_instance():
    iid = 'i-0ff0b215fa94eb081'
    bt3 = boto3.session.Session(profile_name=profile, region_name=region)
    res = terminate_ec2_instance(bt3=bt3, instance_id=iid)
    delete_ssh_key(bt3, 'test-script-asd913fjgq3')
    # deletes secruity group on ec2
    delete_secruity_group(bt3, 'sg-0aa1ef3fe21dde160	')
    assert res == True
