import boto3


def get_boto3_client(args):
    try:
        args['bt3'] = boto3.session.Session(
            profile_name=args['aws_profile'], region_name=args['aws_region'])
        return args
    except Exception as e:
        raise(e)
