import paramiko
from io import StringIO

def createSSHClient(key, ec2_username='ec2-user', public_dns_name=''):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        pkey = paramiko.RSAKey.from_private_key(StringIO(key['value']))
        ssh.connect(public_dns_name, username=ec2_username, pkey=pkey)
        return ssh
    except Exception as e:
        raise(e)
