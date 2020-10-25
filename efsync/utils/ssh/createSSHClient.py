import paramiko


def createSSHClient(key, ec2_username='ec2-user', public_dns_name=''):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        privkey = paramiko.RSAKey.from_private_key(key['value'])
        ssh.connect(public_dns_name, username=ec2_username, pkey=privkey)
        return ssh
    except Exception as e:
        raise(e)
