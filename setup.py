from setuptools import setup, find_packages
from setuptools.command.install import install
import gzip
import tempfile
import tarfile
import subprocess
import shutil
import urllib.request
from io import BytesIO

# Taken from the LKH website at http://akira.ruc.dk/~keld/research/LKH/
LKH = 'http://akira.ruc.dk/~keld/research/LKH/LKH-2.0.9.tgz'

def install_lkh(scripts):
    print('Downloading and installing LKH from ' + LKH)
    content = urllib.request.urlopen(LKH).read()
    with tempfile.TemporaryDirectory() as d:
        with tarfile.open(fileobj=BytesIO(gzip.decompress(content))) as tf:
            tf.extractall(d)
        
        subdir = d + '/LKH-2.0.9'
        subprocess.run('cd ' + subdir + ' && make', shell=True, check=True)

        print('LKH will be installed into ' + scripts)
        shutil.copy(subdir + '/LKH', scripts)


class PostInstallCommand(install):
    def run(self):
        install_lkh(self.install_scripts)
        install.run(self)


setup(
    name='seriate',
    version='0.1',
    description='Simple seriation of data series',
    author='Andy Jones',
    author_email='andyjones.ed@gmail.com',
    url='https://github.com/andyljones/seriate',
    packages=find_packages(),
    cmdclass={'install': PostInstallCommand})
