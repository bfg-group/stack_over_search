# stack_over_search
*Для запуска скопировать себе в любую папку*<br/>
<br/>
**StackOversearch.py** - основной файл, им запускается наше веб-приложение <br />
**StackMysql.py** - содержит методы для работы с MySQL <br />
**renewer.py** - запускается отдельно (просто запускается), обновляет информацию по запросам <br />
<br /> 
**Зависимости:** <br />
redis-server >= 2:3.0.6-1 <br />
mysql-server >= 5.7.19-0ubuntu0.16.04.1
# Описание настроек
**[renewer_settings]**
* ws_ip = {ip адрес: 127.0.0.1}
* ws_port = {порт: 8081}
* work_timeout = {время (сек): 60}
* time_between_request = {время (сек): 10}
* msg_appear_time = {время (сек): 15} 

**[search_settings]**
* cache_timeout = 60

**[redis]**
* ip = {ip адрес: 127.0.0.1}
* port = 6379

**[mysql]**
* ip = {ip адрес: 127.0.0.1}
* user = {Ваш логин: root}
* password = {Ваш пароль: password}
* db = {Имя используемой базы данных: stack_exchange}

**[logs]**
* level = {Доступные уровни: DEBUG, INFO, ERROR, DISASTER}
* path = {Директория для хранения логов: /var/log }
