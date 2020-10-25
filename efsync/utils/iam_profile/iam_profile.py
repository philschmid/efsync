import json


def create_iam_profile(config: dict = None,retry=False):
    """
    create the instance profile
    both instance_profile and role have the same same so instance profile can be
    deleted from the console. Source:
    http://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_manage_delete.html
    """
    instance_profile = 'efsync_instance_profile_role'
    role = 'efsync_role'
    policy_name = 'efsync_policy'
    policy = {"Statement": []}
    try:
        iam_client = config['bt3'].client('iam')
        if 's3_bucket' in config:
            policy["Statement"].append({
                "Effect": "Allow",
                "Action": ["s3:*"],
                "Resource": [f"arn:aws:s3:::{config['s3_bucket']}",f"arn:aws:s3:::{config['s3_bucket']}/*"]
            })
        policy["Statement"].append({
            "Effect": "Allow",
            "Action": [
                "ec2:DeleteTags",
                "ec2:CreateTags",
            ],
            "Resource": "*"
        })

        trust_policy_ec2 = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {
                        "Service": "ec2.amazonaws.com"
                    },
                    "Action": "sts:AssumeRole"
                }
            ]
        }

        instance_profile = iam_client.create_instance_profile(
            InstanceProfileName=instance_profile
        )
        # create the role, associated with the chosen trust policy
        iam_client.create_role(
            RoleName=role,
            AssumeRolePolicyDocument=json.dumps(trust_policy_ec2, indent=2)
        )

        # attach policy to role
        iam_client.put_role_policy(
            RoleName=role,
            PolicyName=policy_name,
            PolicyDocument=json.dumps(policy, indent=2)
        )

        # associate role and instance profile
        iam_client.add_role_to_instance_profile(
            InstanceProfileName=instance_profile['InstanceProfile']['InstanceProfileName'],
            RoleName=role
        )
        IamInstanceProfile = {
            'Arn': instance_profile['InstanceProfile']['Arn'],
            'Name': instance_profile['InstanceProfile']['InstanceProfileName']
        }
        return IamInstanceProfile
    except Exception as e:
        res = delete_iam_profile(config)
        if res and retry == False:
            return create_iam_profile(config,True)
        else:
            raise(e)

        # iam_client = config['bt3'].client('iam')
        # try:
        #     instance_profile = iam_client.get_instance_profile(
        #         InstanceProfileName=instance_profile
        #     )
        #     IamInstanceProfile = {
        #         'Arn': instance_profile['InstanceProfile']['Arn'],
        #         'Name': instance_profile['InstanceProfile']['InstanceProfileName']
        #     }
        #     return IamInstanceProfile
        # except Exception as e:
        #     print(e)
        #     raise(e)


def delete_iam_profile(config: dict = None):
    try:
        iam_client = config['bt3'].client('iam')
        # accound_id = bt3.client('sts').get_caller_identity().get('Account')
        instance_profile = 'efsync_instance_profile_role'
        role = 'efsync_role'
        policy_name = 'efsync_policy'

        iam_client.remove_role_from_instance_profile(
            InstanceProfileName=instance_profile,
            RoleName=role
        )

        iam_client.delete_instance_profile(
            InstanceProfileName=instance_profile
        )

        iam_client.delete_role_policy(
            RoleName=role,
            PolicyName=policy_name
        )

        iam_client.delete_role(
            RoleName=role
        )

        return True
    except Exception as e:
        print(e)
        raise(e)
