from setuptools import setup

setup(
    name='todo-application',
    packages=['app'],
    include_package_data=True,
    install_requires = ['flask',],
)