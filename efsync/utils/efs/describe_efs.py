

def describe_file_systems(bt3, file_system_id: str) -> bool:
    efs_client = bt3.client('efs')
    response = efs_client.describe_file_systems(
        MaxItems=1,
        FileSystemId=file_system_id
    )
    if response['FileSystems'][0]['NumberOfMountTargets'] > 0:
        return True
    else:
        return False
