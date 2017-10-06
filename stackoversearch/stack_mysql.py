import pymysql.cursors
import logging
from configparser import ConfigParser


config = ConfigParser()
config.read('/etc/stackoversearch/stack_settings.ini')

logfile = config.get('logs', 'path')
loglevel = config.get('logs', 'level').upper()


# Выставляем уровень для logger
def get_log_level(loglevel):
    level = logging.DEBUG if loglevel == "INFO" else None
    level = logging.INFO if loglevel == "INFO" else None
    level = logging.ERROR if loglevel == "ERROR" else None
    level = logging.DISASTER if loglevel == "DISASTER" else None
    if level is None:
        level = logging.ERROR
    return level


level = get_log_level(loglevel)

logging.basicConfig(filename=logfile+'/mysql_error.log',
                    format='[%(asctime)s] - %(lineno)d - %(message)s',
                    level=level)
logger = logging.getLogger()


class SQLRequest():
    def __init__(self):
        self.connection = pymysql.connect(host=config.get('mysql', 'ip'),
                                          user=config.get('mysql', 'user'),
                                          password=config.get('mysql', 'password'),
                                          db=config.get('mysql', 'db'),
                                          charset='utf8',
                                          cursorclass=pymysql.cursors.DictCursor)

    def get_req_list(self, **kwargs):
        """
        Метод для получения списка всех сделанных запросов
        """
        try:
            with self.connection.cursor() as self.cur:
                select = """SELECT `request`, `reqtime` FROM requests"""
                # Сортируем, если попросят
                sort_or_not = kwargs.pop('sort', '')
                if sort_or_not is True:
                    select = select + """ ORDER BY `reqtime` DESC"""
                self.cur.execute(select)
                results = self.cur.fetchall()
        except Exception as err:
            logger.error(err)
        finally:
            self.cur.close()
            return results

    def get_last_req_activity(self, name):
        """
        Метод для получения времени последней активности
        в unixtime по имени запроса
        """
        try:
            with self.connection.cursor() as self.cur:
                self.cur.execute("""SELECT UNIX_TIMESTAMP(last_activity)
                                    FROM requests_data
                                    WHERE request = %s
                                    ORDER BY `last_activity` DESC
                                    LIMIT 1""", (name))
                last_activity = self.cur.fetchone()
        except Exception as err:
            logger.error(err)
        finally:
            self.cur.close()
            return last_activity

    def record_intitle_to_mysql(self, intitle):
        """
        Метод для записи запроса в mysql
        """
        try:
            with self.connection.cursor() as self.cur:
                self.cur.execute("""INSERT INTO requests (request, reqtime)
                                    VALUES(%s, NOW())
                                    ON DUPLICATE KEY UPDATE reqtime=NOW()""",
                                    (intitle))
                self.connection.commit()
        except Exception as err:
            logger.error(err)
        finally:
            self.cur.close()

    def record_response(self, intitle, response):
        """
        Метод для записи полученных от API значений в mysql
        """
        for i in range(0, len(response) - 1):
            try:
                with self.connection.cursor() as self.cur:
                        title = response[i]['title']
                        author = response[i]['owner']['display_name']
                        link = response[i]['link']
                        creation_date = response[i]['creation_date']
                        last_activity = response[i]['last_activity_date']

                        self.cur.execute("""INSERT INTO `requests_data` (`request`, `title`, `author`, `link`, `create_date`, `last_activity`)
                                            VALUES(%s, %s, %s, %s, FROM_UNIXTIME(%s), FROM_UNIXTIME(%s))
                                            ON DUPLICATE KEY UPDATE last_activity=FROM_UNIXTIME(%s)""",
                                            (intitle, title, author, link, creation_date, last_activity, last_activity))

                        self.connection.commit()
            except Exception as err:
                logger.error(err)
            finally:
                self.cur.close()

    def results_for_print(self, params_dict):
        """
        Метод забирает результаты для генерации
        страницы с ответами на запрос из базы
        """

        intitle = params_dict['intitle']
        pagesize = params_dict['pagesize']
        page = params_dict['page']

        try:
            with self.connection.cursor() as self.cur:
                self.cur.execute("""SELECT CAST((@row_number:=@row_number + 1) AS SIGNED) AS num, title, author, link, create_date, last_activity
                                    FROM requests_data, (SELECT @row_number:=%s) AS t
                                    WHERE request = %s
                                    ORDER BY last_activity DESC
                                    LIMIT %s OFFSET %s""",
                                    (int(pagesize)*(page - 1), intitle, int(pagesize), int(pagesize)*(page - 1)))
                results = self.cur.fetchall()
        except Exception as err:
            logger.error(err)
        finally:
            self.cur.close()
            return results

    def __del__(self):
        try:
            self.connection.close()
        except Exception as err:
            logger.error(err)
