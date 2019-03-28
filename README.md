# stack_over_search
Пример решения тестового задания (файл tsk.pdf) на языке python3.6.

### Процесс установки
+ Пулим репозиторий
+ Заходим в папку cd ./stack_over_search
+ Создаем виртуальное окружение virtualenv в папке с проектом, переключаемся на него
+ Устанавливаем командой pip install -e ./stack_over_search
+ После успешной установки пакета вебсервер запустится консольной командой stack_start
+ После успешной установки пакета фоновый обработчик запустится консольной командой renewer_start<br>
# Зависимости:
+ redis-server >= 2:3.0.6-1 <br>
+ mysql-server >= 5.7.19-0ubuntu0.16.04.1<br>
# Подготовка mysql
Для работы нам потребуется mysql. Настройки указываются в отдельном .ini файле, о нем позже.<br>
В файле tables.sql находится sql код для создания необходимых для работы приложения таблиц **requests** и **requests_data**. <br>
Кодировку для таблиц взял utf8mb4, т.к. на StackOverflow в тему можно вставлять (дада, о боже) смайлики!

# Описание файлов
**stack_oversearch.py** - основной файл, здесь вся логика страниц и запуск вебсервера <br>
**stack_mysql.py** - содержит методы для работы с MySQL <br>
**renewer.py** - робот, обновляющий информацию по ранее выполненым запросам <br>
**stack_logs.py** - настройки для logger


# Описание настроек
*Лежат в /etc/stackoversearch/stack_settings.ini*<br>

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
* path = {Директория для хранения логов: /etc/stackoversearch/logs }


