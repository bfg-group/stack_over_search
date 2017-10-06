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
<hr />
# Описание настроек
[renewer_settings] <br>
ws_ip = {ip адрес: 127.0.0.1} <br />
ws_port = {порт: 8081} <br />
work_timeout = {время (сек): 60} <br />
time_between_request = {время (сек): 10} <br />
msg_appear_time = {время (сек): 15} <br / >
<br / >
[search_settings]<br / >
cache_timeout = 60<br / >
<br / >
[redis]
ip = 127.0.0.1<br / >
port = 6379
<br / >
[mysql]
ip = 127.0.0.1<br / >
user = root<br / >
password = password<br / >
db = stack_exchange<br / >
<br / >
[logs]<br / >
level = INFO<br / >
path = /var/log/<br / >
