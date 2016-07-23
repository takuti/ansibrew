from setuptools import setup

setup(
    name='ansibrew',
    version='0.2.0',
    py_modules=['ansibrew'],
    install_requires=['Click'],
    entry_points='''
        [console_scripts]
        ansibrew=ansibrew:cli
    ''',
)
