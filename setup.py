from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in app_perfiles/__init__.py
from app_perfiles import __version__ as version

setup(
	name='app_perfiles',
	version=version,
	description='Aplicacion para administrar postulaciones .',
	author='Carolina Fonseca',
	author_email='caro-fonseca@outlook.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
