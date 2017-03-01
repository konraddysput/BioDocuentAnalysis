from Cython.Build import cythonize
from setuptools import setup, find_packages, Extension

from queryexpander import __version__

extensions = [
    Extension(
        'queryexpander.semantic_similarity',
        ['queryexpander/semantic_similarity.pyx'],
        libraries=['accelerator'],
        language='c++',
        extra_compile_args=['-std=c++1z', '-O3', '-fopenmp',
                            '-I./libraries/document-search-accelerator/libraries/cpp_redis/includes',
                            '-I./libraries/document-search-accelerator/libraries/cpp_redis/tacopie/includes',
                            '-I./libraries/document-search-accelerator/libraries/fmt'],
        extra_link_args=['-std=c++1z', '-fopenmp', '-L./libraries/document-search-accelerator/build/lib'],
    ),
]

setup(
    name='TipsterDataLoader',
    version=__version__,
    packages=find_packages(),
    include_package_data=True,

    entry_points={
        'console_scripts': [
            'TipsterDataLoader = queryexpander.__main__:cli',
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
