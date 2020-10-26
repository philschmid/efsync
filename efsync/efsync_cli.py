from argparse import ArgumentParser
from efsync.main import efsync


def main():
    # Initiate the parser with a description
    parser = ArgumentParser(
        "efsync CLI tool. More Information read https://github.com/", usage="efsync <command> [<args>]")
    parser.add_argument("--version", "-v",
                        help="show program version", action="store_true")

    parser.add_argument("--requirements", "-r",
                        help="path of your requirements.txt", default="requirements.txt")
    # optional
    parser.add_argument(
        "--config_file", "-cf", help="path of your efsync.yaml")

    parser.add_argument("--python_version", "-py",
                        help="Python version used to install dependencies",
                        default=3.8)

    parser.add_argument("--efs_pip_dir", "-epd",
                        help="directory where the pip packages will be installed on efs",
                        default='lib')

    parser.add_argument("--efs_filesystem_id", "-efi",
                        help="File System ID from the EFS filesystem",
                        )
    parser.add_argument("--clean_efs", "-ce",
                        help="Defines if the efs should be cleaned up before uploading",
                        default=True)

    parser.add_argument("--file_dir", "-fd",
                        help="directory where all other files will be placed",
                        default='tmp')

    parser.add_argument("--aws_profile", "-ap",
                        help="name of the used AWS profile",
                        default='efsync')

    parser.add_argument("--aws_region", "-ar",
                        help="aws region where the efs is running",
                        default='eu-central-1')

    parser.add_argument("--subnet_Id", "-sbd",
                        help="subnet id of the efs ")

    parser.add_argument("--ec2_key_name", "-ekn",
                        help="temporary key name for the ec2 instance")

    parser.add_argument("--file_dir_on_ec2", "-fdoe",
                        help="name of the directory where your file from <file_dir> will be uploaded")

    parser.add_argument("--s3_bucket", "-s3b",
                        help="s3 bucket name from where the files will be downloaded")

    parser.add_argument("--s3_keyprefix", "-s3k",
                        help="s3 keyprefix of the directory in s3. Files will be downloaded")

    args = parser.parse_args()
    args_dict = vars(args)
    for k, v in dict(args_dict).items():
        if v is None:
            del args_dict[k]
    efsync(args_dict)


if __name__ == "__main__":
    main()
