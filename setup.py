from setuptools import setup, find_packages

from dataloader import __version__

setup(
    name='TipsterDataLoader',
    version=__version__,
    packages=find_packages(),
    include_package_data=True,

    entry_points={
        'console_scripts': [
            'TipsterDataLoader = dataloader.__main__:cli',
        ],
    },

    install_requires=[
        'pymongo',
        'click',
    ],
)
