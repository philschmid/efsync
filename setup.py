from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

print(find_packages())

setup(
    name='efsync',
    version='1.0.3',
    packages=find_packages(),
    entry_points={
        "console_scripts": ["efsync=efsync.efsync_cli:main"]
    },
    author="Philipp Schmid",
    author_email="schmidphilipp1995@gmail.com",
    description="A CLI/SDK which automatically uploads pip packages and directories to aws efs to be used in aws lambda",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/philschmid",
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'scp',
        'paramiko',
        'boto3',
        'pyaml'
    ],
)
