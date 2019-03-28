from .stack_mysql import SQLRequest
from .stack_logs import stack_logger
from aiohttp import web
import aiohttp_jinja2
import jinja2
import redis
import requests
from configparser import ConfigParser


config = ConfigParser()
config.read('/etc/stackoversearch/stack_settings.ini')

logger = stack_logger()

try:
    r = redis.StrictRedis(host=config.get('redis', 'ip'),
                          port=config.getint('redis', 'port'),
                          db=0,
                          decode_responses=True,
                          charset="utf-8")
except Exception as err:
    logger.error(err)


class StackApiReq():
    def __init__(self, name, pagesize, page):
        self.intitle = name
        self.order = 'desc'
        self.sort = 'creation'
        self.pagesize = pagesize
        self.page = page
        self.has_more = True

    def make_req(self):
        """
        Метод для получения данных от
        API согласно параметрам созданого объекта
        """

        api_link = "http://api.stackexchange.com/2.2/search"
        data = {'page': str(self.page),
                'pagesize': self.pagesize,
                'order': self.order,
                'sort': self.sort,
                'intitle': self.intitle,
                'site': 'stackoverflow'}

        httpreq = requests.get(api_link, params=data)
        response = httpreq.json()
        try:
            self.has_more = response['has_more']
        except KeyError:
            logger.error('Некорректный ответ от API:', response)
        return response


def main(request):
    """
    Функция для рендеринга основной страницы поиска.
    На ней получаем от юзера данные - запрос/кол-во ответов на страницe
    """
    MySQLReq = SQLRequest()

    context = {}

    # Получаем данные формы
    data = request.query
    try:
        intitle = data['intitle']
        page_number = data['page_number']
    except KeyError:
        # Если данных о формах нет - рендерим чистую страницу
        return aiohttp_jinja2.render_template('search.html',
                                              request,
                                              context)

    # Если данных формы не хватает - рендерим ошибку
    if intitle == '' or page_number == '':
        context['error'] = "Не переданы обязательные параметры"
        return aiohttp_jinja2.render_template('search.html',
                                              request,
                                              context)

    # Если всё ок - выполняем запрос
    else:
        try:
            page = int(data['page'])
        except TypeError:
            page = 1

        # Создаем объект пользовательского запроса и логируем действие в базу
        UserReq = StackApiReq(intitle, page_number, page)

        results = []

        # Cчитаем индексы первой и последней строки на странице
        first_index = (UserReq.page - 1) * int(UserReq.pagesize) + 1
        last_index = UserReq.page * int(UserReq.pagesize)

        redis_name = '{}:{}:results:'.format(UserReq.intitle, UserReq.pagesize)

        # Если есть в кэше - достаем, нет - берем из базы и кладем в кэш
        if r.hgetall(redis_name + str(last_index)):
            logger.debug('req_cache')
            for i in range(first_index, last_index + 1):
                results.append(r.hgetall(redis_name + str(i)))

        else:
            logger.debug('req_new')
            api_data = UserReq.make_req()
            try:
                api_data = api_data['items']
            except KeyError:
                context['error'] = 'Ошибка API: ' + api_data['error_message']
                return aiohttp_jinja2.render_template('search.html',
                                                      request,
                                                      context)

            MySQLReq.record_response(UserReq.intitle, api_data)
            results = MySQLReq.results_for_print(UserReq.__dict__)

            i = first_index
            for row in results:
                timeout = config.getint('search_settings', 'cache_timeout')
                r.hmset(redis_name + str(i), row)
                r.expire(redis_name + str(i), timeout)
                i += 1

        context = {'request_data': results,
                   'intitle': UserReq.intitle,
                   'pagesize': UserReq.pagesize,
                   'page': str(UserReq.page)}

        # Значения для кнопочек Назад/Вперед
        if page > 1:
            context['prev_page'] = page - 1
        if UserReq.has_more is True:
            context['next_page'] = page + 1

        # Чистим кэш по списку запросов в редисе
        response = r.keys('showall:*')
        for row in response:
            r.delete(row)

        MySQLReq.record_intitle_to_mysql(UserReq.intitle)
        MySQLReq.__del__

        return aiohttp_jinja2.render_template('show.html',
                                              request,
                                              context)


def show_all(request):
    """
    Функция рендеринга списка всех запросов.
    Ходим в базу, смотрим существующие запросы.
    При необходимости сортируем
    """
    MySQLReq = SQLRequest()

    # Обнуляем словарь с данными для передачи веб странице
    context = {}

    # Получаем данные формы
    data = request.query
    try:
        sort = data['sort']
    except KeyError:
        sort = ''

    if sort != '':
        if r.hgetall('showall:sorted:results:1'):
            logger.debug('sorted cache')
            results = load_show_all_from_cache('sorted:')
        else:
            logger.debug('sorted new')
            results = MySQLReq.get_req_list(sort=True)
            send_show_all_to_cache(results, sort=True)

    else:
        if r.hgetall('showall:results:1'):
            logger.debug('cache')
            results = load_show_all_from_cache('')
        else:
            logger.debug('new')
            results = MySQLReq.get_req_list()
            send_show_all_to_cache(results)

    context['req_records'] = results
    MySQLReq.__del__
    return aiohttp_jinja2.render_template('show_all.html',
                                          request,
                                          context)


def send_show_all_to_cache(results, **kwargs):
    """
    Вспомогательная функция для станицы show_all.
    Складывает запрос к базе в кэш
    """
    sort_or_not = kwargs.pop('sort', '')
    i = 0
    for row in results:
        order = 'sorted:' if sort_or_not else ''
        row_name = 'showall:{}results:{}'.format(order, str(i))
        timeout = config.getint('search_settings', 'cache_timeout')
        r.hmset(row_name, row)
        r.expire(row_name, timeout)
        i += 1


def load_show_all_from_cache(order):
    """
    Вспомогательная функция для станицы show_all
    Если запрос есть в кэше, достаёт его оттуда
    """
    results = []
    response = r.keys('showall:{}results:*'.format(order))
    for i in range(0, len(response)-1):
        results.append(r.hgetall('showall:{}results:{}'.format(order, str(i))))
    return results


# Объявляем всё необходимое для работы aiohttp
app = web.Application()
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('stackoversearch/templates'))
app.router.add_static('/static', path=str('stackoversearch/static'), name='static')

app.router.add_route('*', '/', main)
app.router.add_route('GET', '/show_all', show_all)


def web_server():
    web.run_app(app, host='127.0.0.1', port=8080)


if __name__ == "__main__":
    web_server()
