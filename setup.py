from setuptools import setup, find_packages

setup(
    name='etl_football_transfer',
    version='0.0.1',
    packages=find_packages('src'),
    package_dir={'': 'src'},
)