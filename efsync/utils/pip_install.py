import os
import subprocess
import shutil


def pip_install_requirements(file='requirements.txt', python_version='', pip_dir='', default_dir=".efsync"):
    try:
        shutil.rmtree(f"{default_dir}/{pip_dir}")
        os.mkdir(f"{default_dir}/{pip_dir}")
    except Exception as e:
        raise(e)
    try:
        process = subprocess.run([f' docker run -v "$PWD":/var/task lambci/lambda:build-python{python_version} pip3 --no-cache-dir install -t {default_dir}/{pip_dir} -r {file}'],
                                 shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        if('Installing collected packages' in process.stdout):
            return True
        elif ('Cannot connect' in process.stderr):
            raise RuntimeError(process.stderr)
        else:
            raise RuntimeError(
                'something went wrong either docker not running or no requirements file')
    except Exception as e:
        raise RuntimeError(
            'something went wrong either docker not running or no requirements file')


# docker run -it -v "$PWD":/var/task lambci/lambda:build-python3.8 bash
# docker run -it -v "$PWD":/var/task lambci/lambda:build-python3.8 pip3 --no-cache-dir install -t .efsync/lib -r requirements.txt
