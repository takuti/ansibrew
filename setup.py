from setuptools import setup

setup(
    name='ansibrew',
    version='0.1',
    py_modules=['ansibrew'],
    install_requires=[
        'Click',
        'pyyaml'
    ],
    entry_points='''
        [console_scripts]
        ansibrew=ansibrew:cli
    ''',
)
