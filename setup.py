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
    ],
    entry_points={
        'console_scripts': [
            f'{_NAME}_init_db = '
            f'{_NAME}_web_server = {_NAME}.stack_oversearch:web_server',
            f'{_NAME}_update_daemon = {_NAME}.renewer:main',
        ]
    }
)
