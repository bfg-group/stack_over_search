# Описание файлов
**stack_oversearch.py** - основной файл, здесь вся логика страниц и запуск вебсервера
**stack_mysql.py** - содержит методы для работы с MySQL
**renewer.py** - робот, обновляющий информацию по ранее выполненым запросам
<br>
# Зависимости:
redis-server >= 2:3.0.6-1 <br>
mysql-server >= 5.7.19-0ubuntu0.16.04.1
# Описание настроек
*Лежат в /etc/stackoversearch/stack_settings.ini
**[renewer_settings]**
* ws_ip = {ip адрес: 127.0.0.1}
* ws_port = {порт: 8081}
* work_timeout = {время (сек): 60}
* time_between_request = {время (сек): 10}
* msg_appear_time = {время (сек): 15}
**[search_settings]**
* cache_timeout = {время (сек): 60}
**[redis]**
* ip = {ip адрес: 127.0.0.1}
* port = {порт: 6379}

**[mysql]**
* ip = {ip адрес: 127.0.0.1}
* user = {Ваш логин: root}
* password = {Ваш пароль: password}
* db = {Имя используемой базы данных: stack_exchange}

**[logs]**
* level = {Доступные уровни: DEBUG, INFO, ERROR, DISASTER}
* path = {Директория для хранения логов: /var/log }


