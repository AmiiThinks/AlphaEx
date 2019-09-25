from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='alphaex',
    version='0.1.0',
    description='sweeper and plotter',
    long_description=readme,
    author='Yi Wan',
    author_email='umichyiwan@gmail.com',
    url='https://github.com/umichyiwan/experimenter',
    license=license,
    packages=find_packages(exclude=('test')),
    install_requires=[
        'matplotlib'
    ]
)
