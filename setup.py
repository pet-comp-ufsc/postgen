from setuptools import setup, find_packages

VERSION = '0.1'

setup(
    name='postgen',
    version=VERSION,
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'postgen = system.__main__:run',
        ],
    },
    install_requires=[
        'pillow>=5.1',
        'cairosvg>=0.9.0',
    ],
)
