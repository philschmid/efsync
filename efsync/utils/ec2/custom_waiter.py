import boto3
import time


def custom_waiter(config, instance_id):
    try:
        """Polls the ec2 instance tags until there is tag user_data finished. The tag will be set during user_data"""
        ec2_resource = config['bt3'].resource('ec2')
        retry = 0
        while True:
            # gets instance information
            ec2instance = ec2_resource.Instance(instance_id)
            # checks if tags are available
            if ec2instance.tags != None:
                # checks if user_data tag is true
                for tags in ec2instance.tags:
                    if tags['Key'] == 'user_data' and tags['Value'] == 'True':
                        break
                break
            # counts 1 retry up
            retry += 1
            # if it failed 10 times it breaks
            if retry >= 20:
                break
            time.sleep(30)
        # returns true oder false depending on success
        if retry >= 20:
            return False
        else:
            return True
    except Exception as e:
        print(e)
        raise(e)
