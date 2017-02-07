from Cython.Build import cythonize
from setuptools import setup, find_packages, Extension

from dataloader import __version__

extensions = [
    Extension(
        'dataloader.semantic_similarity',
        ['dataloader/semantic_similarity.pyx'],
        libraries=['accelerator'],
        language='c++',
        extra_compile_args=['-std=c++1z', '-O3', '-fopenmp'],
        extra_link_args=['-std=c++1z', '-fopenmp', '-L./libraries/document-search-accelerator/build'],
    ),
]

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
        'pandas',
        'scipy',
        'cython',
        'redis',
    ],

    ext_modules=cythonize(extensions)
)
