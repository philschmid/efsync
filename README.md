# efsync

[![Downloads](https://pepy.tech/badge/efsync)](https://pepy.tech/project/efsync) [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1G4LTw7aW5CBlFHVeiR12r5_49Z_CcEIo?usp=sharing) ![pypi package deployment](https://github.com/philschmid/efsync/workflows/pypi%20package%20deployment/badge.svg) [![PyPI version fury.io](https://badge.fury.io/py/ansicolortags.svg)](https://pypi.python.org/pypi/efsync/)

efsync is an CLI tool/ sdk to automatically upload files and dependencies to AWS EFS. The CLI is easy to use, you only need access to an AWS Account, an AWS EFS-filesystem up and running, and Docker installed. I wrote an article with an complete walkthrough. you can check this one out [here](https://www.philschmid.de/) or simply start with the [Quick Start](#quick-start).

# Documentation

<img align="right" width="600" src="./cli.png" />

- [Quick Start](#quick-start)
- [Examples](#examples)
- [SDK](#SDK)
- [CLI](#cli)

## <a name="quick-start"></a>Quick Start

Example in Google Colab. [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1G4LTw7aW5CBlFHVeiR12r5_49Z_CcEIo?usp=sharing)

1. **Install via pip3**

```bash
pip3 install efsync
```

2.  **sync your pip packages or files to AWS EFS**

```bash
efsync -cf efsync.yaml
```

## <a name="examples"></a>Examples

## CLI Example with `efsync.yaml`

**sync your pip packages or files to AWS EFS**

```bash
efsync -cf efsync.yaml
```

## CLI Example with parameter

**sync your pip packages or files to AWS EFS**

```bash
efsync -r requirements.txt -py 3.8 -epd lib -fd tmp -fdoe tmp -ap schueler -ar eu-central-1 -sbd <subnet_id> -ekn <ec2-key-name>  -efi  <efs_filesystem_id>
```

## SDK Example with `efsync.yaml`

**1. create an configuration file `efsync.yaml`**

```yaml
# lambda ci python version for pip installation
python_version: 3.8
# pip directory on ec2
efs_pip_dir: lib
# extra directory for file upload like ML models
file_dir: dir
# name of the directory where your file from <file_dir> will be uploaded
file_dir_on_ec2: ml
# requirements file
requirements: requirements.txt
# Defines if the efs should be cleaned up before uploading
clean_efs: True
# aws profile configuration
aws_profile: efsync
aws_region: eu-central-1

#aws vpc and ec2 shit
efs_filesystem_id: fs-2adfas123
subnet_Id: subnet-xxx
ec2_key_name: efsync-asd913fjgq3
```

**2. sync your pip packages or files to AWS EFS**

```python
from efsync import efsync

efsync('efsync.yaml')
```

## <a name="cli"></a>CLI

| cli_short | cli_long            | default          | description                                                            |
| --------- | ------------------- | ---------------- | ---------------------------------------------------------------------- |
| -h        | --help              | -                | displays all commands                                                  |
| -r        | --requirements      | requirements.txt | path of your requirements.txt                                          |
| -cf       | --config_file       | -                | path of your efsync.yaml                                               |
| -py       | --python_version    | 3.8              | Python version used to install dependencies                            |
| -epd      | --efs_pip_dir       | lib              | directory where the pip packages will be installed on efs              |
| -efi      | --efs_filesystem_id | -                | File System ID from the EFS filesystem                                 |
| -ce       | --clean_efs         | True             | Defines if the EFS should be cleaned up before uploading               |
| -fd       | --file_dir          | tmp              | directory where all other files will be placed                         |
| -fdoe     | --file_dir_on_ec2   | tmp              | name of the directory where your file from <file_dir> will be uploaded |
| -ap       | --aws_profile       | efsync           | name of the used AWS profile                                           |
| -ar       | --aws_region        | eu-central-1     | aws region where the efs is running                                    |
| -sbd      | --subnet_Id         | -                | subnet id of the efs                                                   |
| -ekn      | --ec2_key_name      | -                | temporary key name for the ec2 instance                                |
