from setuptools import setup

setup(name='stackoversearch',
      version='0.1',
      description='Поиск по сайту StackOverFlow',
      author='Maksim Nabokikh',
      author_email='max.nabokih@gmail.com',
      url='https://github.com/nabokihms/stack_over_search',
      packages=['stackoversearch'],
      include_package_data=True,
      data_files=[('/etc/stackoversearch', ['stackoversearch/stack_settings.ini'])],
      install_requires=['aiohttp==2.3.8',
                        'aiohttp-jinja2==0.14.0',
                        'async-timeout==1.4.0',
                        'configparser==3.5.0',
                        'multidict==3.2.0',
                        'PyMySQL==0.7.11',
                        'redis==2.10.6',
                        'websocket-server==0.4',
                        'requests==2.9.1'],
      entry_points={
        'console_scripts':
        ['stack_start = stackoversearch.stack_oversearch:web_server',
         'renewer_start = stackoversearch.renewer:main']
        }
      )
