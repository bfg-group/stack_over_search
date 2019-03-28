from setuptools import setup, find_packages

_NAME = 'stack_over_search'

setup(
    name=f'{_NAME}',
    version='0.1.0',
    description='Search client for StackOverFlow',
    author='Maksim Nabokikh',
    author_email='max.nabokih@gmail.com',
    url='https://github.com/nabokihms/stack_over_search',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'aiohttp==3.5.4',
        'aiomysql==0.0.20',
        'aioredis==1.2.0',
        'sqlalchemy==1.3.1',
    ],
    entry_points={
        'console_scripts': [
            f'{_NAME}_init_db = {_NAME}.cli:run_init_db',
            f'{_NAME}_web_server = {_NAME}.cli:run_webserver',
            f'{_NAME}_update_daemon = {_NAME}.renewer:main',
        ]
    }
)
