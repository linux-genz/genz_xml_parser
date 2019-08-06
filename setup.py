#/usr/lib/python3
import setuptools

long_dsc = ''
with open('README.md', 'r') as file_obj:
    long_dsc = file_obj.read()

setuptools.setup(
    name='gxp',
    version='0.8',
    author='Zach Volchak',
    author_email='zakhar.volchak@hpe.com',
    description='Converts xml genz specs into a C and Python artifacts.',
    long_description=long_dsc,
    long_description_content_type='text/markdown',
    url='https://github.com/linux-genz/genz_xml_parser',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: POSIX :: Linux',
    ],
)