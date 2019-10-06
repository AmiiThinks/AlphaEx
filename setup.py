from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='alphaex',
    version='0.1.0',
    description='AlphaEx: A Python Toolkit for Managing Large Number of Experiments',
    long_description=readme,
    author='Yi Wan',
    author_email='wan6@ualberta.ca',
    url='https://github.com/yiwan-rl/AlphaEx',
    license=license,
    packages=find_packages(exclude=('test')),
    install_requires=[
        'json', 'numpy'
    ]
)
