

def validate_config(config:dict=None) -> bool:
  """validates if the configuration is valid"""
  # validate if required keys are included
  if all (keys in config for keys in ("efs_filesystem_id","subnet_Id","ec2_key_name","aws_profile","aws_region")):
    pass
  else:
    raise Exception("Required Keys are missing")
  # validate if keys for pip and s3 are included
  if all (keys in config for keys in ("efs_pip_dir","python_version","requirements","s3_bucket","s3_keyprefix","file_dir_on_ec2")):
    pass
  # validate if keys for pip are included
  elif all (keys in config for keys in ("efs_pip_dir","python_version","requirements","file_dir","file_dir_on_ec2")):
    pass
  # validate if keys for pip are included
  elif all (keys in config for keys in ("efs_pip_dir","python_version","requirements")):
    pass
  # validate if keys for scp are included
  elif all (keys in config for keys in ("file_dir","file_dir_on_ec2")):
    pass
  # validate if keys for s3 are included
  elif all (keys in config for keys in ("s3_bucket","s3_keyprefix","file_dir_on_ec2")):
    pass
  else:
    raise Exception("Keys are missing")
  ## test if all keys are != None 
  for k, v in dict(config).items():
    if v is None:
        raise Exception("None values included")
  return True