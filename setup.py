from setuptools import setup
'''
This is need to be able to use the `pip install -e {path}` command
'''
setup(
    name='bookspyne',
    version='1.0',
    entry_points={
        'console_scripts': [
            'bookspyne=bookspyne:handle_inputs'
        ]
    }
)