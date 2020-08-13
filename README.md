badges:

[![Downloads](https://pepy.tech/badge/efsync)](https://pepy.tech/project/efsync) downloads

colab with example

# Documentation

<img align="right" width="400" src="./cli.png" />

- [Quick Start](#quick-start)
- [Examples](#examples)
- [SDK](#SDK)
- [CLI](#cli)

## <a name="quick-start"></a>Quick Start

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
efsync -r requirements.txt -py 3.8 -epd lib -fd tmp -ap schueler -ar eu-central-1 -sbd <subnet_id> -ekn <ec2-key-name>
```

## SDK Example with `efsync.yaml`

**create an configuration file `efsync.yaml`**

```yaml
# lambda ci python version for pip installation
python_version: 3.8
# pip directory
efs_pip_dir: lib
# extra directory for file upload like ML models
dir: dir
# requirements file
requirements: requirements.txt
# aws profile configuration
aws_profile: efsync
aws_region: eu-central-1

#aws vpc and ec2 shit
subnet_Id: subnet-xxx
ec2_key_name: efsync-asd913fjgq3
```

2.  **sync your pip packages or files to AWS EFS**

```python
from efsync import efsync

efsync('efsync.yaml')
```

## <a name="cli"></a>CLI

| cli_short | cli_long         | default          | description                                               |
| --------- | ---------------- | ---------------- | --------------------------------------------------------- |
| -h        | --help           | -                | displays all commands                                     |
| -r        | --requirements   | requirements.txt | path of your requirements.txt                             |
| -cf       | --config_file    | -                | path of your efsync.yaml                                  |
| -py       | --python_version | 3.8              | Python version used to install dependencies               |
| -epd      | --efs_pip_dir    | lib              | directory where the pip packages will be installed on efs |
| -fd       | --file_dir       | tmp              | directory where all other files will be placed            |
| -ap       | --aws_profile    | efsync           | name of the used AWS profile                              |
| -ar       | --aws_region     | eu-central-1     | aws region where the efs is running                       |
| -sbd      | --subnet_Id      | -                | subnet id of the efs                                      |
| -ekn      | --ec2_key_name   | -                | temporary key name for the ec2 instance                   |
