# 🚀 efsync

[![Downloads](https://pepy.tech/badge/efsync)](https://pepy.tech/project/efsync) [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1G4LTw7aW5CBlFHVeiR12r5_49Z_CcEIo?usp=sharing) ![pypi package deployment](https://github.com/philschmid/efsync/workflows/pypi%20package%20deployment/badge.svg) [![PyPI version fury.io](https://badge.fury.io/py/ansicolortags.svg)](https://pypi.python.org/pypi/efsync/)

efsync is an CLI/SDK to automatically upload files and dependencies to AWS EFS. The CLI is easy to use, you only need access to an AWS Account, an AWS EFS-filesystem up and running. I wrote an article with an complete walkthrough. you can check this one out [here](https://www.philschmid.de/) or simply start with the [Quick Start](#quick-start).

i created several examples for every usecase.

![CLI Example](./cli.png)

## Outline

- [Quick Start](#quick-start)
- [Configuration](#sdk)
- [Examples](#examples)
- [CLI](#cli)
- [Connect](#connect)

# 🏃🏻‍♂️ <a name="quick-start"></a>Quick Start

Example in Google Colab. [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1G4LTw7aW5CBlFHVeiR12r5_49Z_CcEIo?usp=sharing)

1. **Install via pip3**

```bash
pip3 install efsync
```

2.  **sync your pip packages or files to AWS EFS**

usage with the cli

```bash
efsync -cf efsync.yaml
```

or with python

```python
from efsync import efsync

efsync('efsync.yaml')
```

# ⚙️ <a name="sdk"></a> Configurations

## Configuration with yaml file `efsync.yaml`

```yaml
#standard configuration
efs_filesystem_id: fs-2adfas123 # aws efs filesystem id (moint point)
subnet_Id: subnet-xxx # subnet of which the efs is running in
ec2_key_name: efsync-asd913fjgq3 # required key name for starting the ec2 instance
clean_efs: all # Defines if the EFS should be cleaned up before. values: `'all'`,`'pip'`,`'file'` uploading
# aws profile configuration
aws_profile: efsync # aws iam profile with required permission configured in .aws/credentials
aws_region: eu-central-1 # the aws region where the efs is running

# pip packages configurations
efs_pip_dir: lib # pip directory on ec2
python_version: 3.8 # python version used for installing pip packages -> should be used as lambda runtime afterwads
requirements: requirements.txt # path + file to requirements.txt which holds the installable pip packages

# s3 config
s3_bucket: my-bucket-with-files # s3 bucket name from files should be downloaded
s3_keyprefix: models/bert # s3 keyprefix for the files
file_dir_on_ec2: ml # name of the directory where your file from <file_dir> will be uploaded

# upload files with scp to efs
file_dir: local_dir # extra local directory for file upload like ML models
```

## Configuration with CLI Parameters

```bash
efsync  --efs_filesystem_id  fs-2adfas123 \
        --subnet_Id subnet-xxx \
        --ec2_key_name efsync-asd913fjgq3 \
        --clean_efs all \
        --aws_profile efysnc \
        --aws_region yo-region-1 \
        --efs_pip_dir lib \
        --python_version 3.8 \
        --requirements requirements.txt \
        --s3_bucket my-bucket-with-files \
        --s3_keyprefix models/bert \
        --file_dir local_dir \
        --file_dir_on_ec2 ml
```

## Configuration with CLI and yaml

```bash
efsync -cf efsync.yaml
```

## Configuration with python dictonary

```python
config = {
  'efs_filesystem_id': 'fs-2adfas123', # aws efs filesystem id (moint point)
  'subnet_Id': 'subnet-xxx', # subnet of which the efs is running in
  'ec2_key_name':'efsync-asd913fjgq3',  # required key name for starting the ec2 instance
  'clean_efs': 'all', # Defines if the EFS should be cleaned up before. values: `'all'`,`'pip'`,`'file'` uploading
  'aws_profile': 'efysnc', # aws iam profile with required permission configured in .aws/credentials
  'aws_region': 'eu-central-1', # the aws region where the efs is running
  'efs_pip_dir': 'lib',  # pip directory on ec2
  'python_version': 3.8,  # python version used for installing pip packages -> should be used as lambda runtime afterwads
  'requirements': 'requirements.txt', # path + file to requirements.txt which holds the installable pip packages
  'file_dir': 'local_dir', # extra local directory for file upload like ML models
  'file_dir_on_ec2': 'ml', # name of the directory where your file from <file_dir> will be uploaded
  's3_bucket': 'my-bucket-with-files', # s3 bucket name from files should be downloaded
  's3_keyprefix': 'models/bert' # s3 keyprefix for the files
}
```

# 🏗 <a name="examples"></a> Examples

I provided several jupyter notebooks with examples. There are examples for installing pip packages only, installing pip packages and downloading files from s3, downloading only files from s3, installing pip packages and uploading files from local with scp and only uploading files with scp

- [installing pip packages](./examples/efsync_pip_packages.ipynb)
- [installing pip packages and downloading files from s3](./examples/efsync_pip_packages_and_s3_files.ipynb)
- [installing pip packages and uploading local files with scp](./examples/efsync_pip_packages_and_scp_files.ipynb)
- [downloading files from s3](./examples/efsync_s3_files.ipynb)
- [uploading local files with scp](./examples/efsync_scp_files.ipynb)

**simplest usage:**

```python
from efsync import efsync

efsync('efsync.yaml')
```

## <a name="cli"></a>CLI Parameteres

| cli_short | cli_long            | default          | description                                                                                |
| --------- | ------------------- | ---------------- | ------------------------------------------------------------------------------------------ |
| -h        | --help              | -                | displays all commands                                                                      |
| -r        | --requirements      | requirements.txt | path of your requirements.txt                                                              |
| -cf       | --config_file       | -                | path of your efsync.yaml                                                                   |
| -py       | --python_version    | 3.8              | Python version used to install dependencies                                                |
| -epd      | --efs_pip_dir       | lib              | directory where the pip packages will be installed on efs                                  |
| -efi      | --efs_filesystem_id | -                | File System ID from the EFS filesystem                                                     |
| -ce       | --clean_efs         | -                | Defines if the EFS should be cleaned up before. values: `'all'`,`'pip'`,`'file'` uploading |
| -fd       | --file_dir          | tmp              | directory where all other files will be placed                                             |
| -fdoe     | --file_dir_on_ec2   | tmp              | name of the directory where your file from <file_dir> will be uploaded                     |
| -ap       | --aws_profile       | efsync           | name of the used AWS profile                                                               |
| -ar       | --aws_region        | eu-central-1     | aws region where the efs is running                                                        |
| -sbd      | --subnet_Id         | -                | subnet id of the efs                                                                       |
| -ekn      | --ec2_key_name      | -                | temporary key name for the ec2 instance                                                    |
| -s3b      | --s3_bucket         | -                | s3 bucket name from where the files will be downloaded instance                            |
| -s3k      | --s3_keyprefix      | -                | s3 keyprefix of the directory in s3. Files will be downloaded recursively                  |

# <a name="connect"></a> 🔗 Connect with me

<a href="https://www.philschmid.de" target="_blank"><img alt="Personal Website" src="https://img.shields.io/badge/Personal%20Website-%2312100E.svg?&style=for-the-badge&logoColor=white" /></a>
<a href="https://twitter.com/_philschmid" target="_blank"><img alt="Twitter" src="https://img.shields.io/badge/twitter-%231DA1F2.svg?&style=for-the-badge&logo=twitter&logoColor=white" /></a>
<a href="https://medium.com/@schmidphilipp1995" target="_blank"><img alt="Medium" src="https://img.shields.io/badge/medium-%2312100E.svg?&style=for-the-badge&logo=medium&logoColor=white" /></a>
<a href="https://www.linkedin.com/in/philipp-schmid-a6a2bb196" target="_blank"><img alt="LinkedIn" src="https://img.shields.io/badge/linkedin-%230077B5.svg?&style=for-the-badge&logo=linkedin&logoColor=white" /></a>

# 🏥 Contributing

If you want to contribute be sure to review the contributions guidelines.

# 📃 License

A copy of the License is provided in the LICENSE file in this repository.
