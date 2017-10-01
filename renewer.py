from StackMysql import SQLRequest
from StackOversearch import StackApiReq
from websocket_server import WebsocketServer
import time
import threading
import logging
from configparser import ConfigParser

logging.basicConfig(filename='/var/log/renewer.log',
                    format = '%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
                    level = logging.DEBUG)
logger = logging.getLogger()

config = ConfigParser()
config.read('StackSettings.ini')

ws_port = config.getint('renewer_settings', 'ws_port')
ws_ip = config.get('renewer_settings', 'ws_ip')
server = WebsocketServer(ws_port, host=ws_ip)


def web_socket_msg():
    """ Запускаем сервер для WebSocket"""
    global server
    server.run_forever()


def send_msg():
    """Проверяем, необходим ли апдейт по запросам.
       Если необходим - делаем и шлем об этом сообщение
       через WebSocket."""
    global server
    MySQLReq = SQLRequest()
    while True:
        message = {}
        requests_list = MySQLReq.get_req_list()

        for request in requests_list:
            req_timeout = config.getint('renewer_settings', 'time_between_request')
            time.sleep(req_timeout)

            last_activity = MySQLReq.get_last_req_activity(request['request'])

            logger.debug('START:', request['request'])
            logger.debug('LAST ACTIVITY:', last_activity)

            message[request['request']] = 0
            data_to_update = []

            # Инкремент используем в качестве номера страницы
            # Если на странице всем строкам нужен апдейт - смотрим следующую
            i = 1
            while True:
                UserReq = StackApiReq(request['request'], "100", i)
                try:
                    items = UserReq.make_req()['items']
                except KeyError:
                    logger.error('Нет данных от API')
                    break

                # Для всех строк полученных от апи сравниваем дату последней активности
                # Если больше - апдейтим, меньше - заканчиваем цикл
                for number in range(0, len(items) - 1):
                    if items[number]['last_activity_date'] > last_activity['UNIX_TIMESTAMP(last_activity)']:
                        logger.debug('UPDATE:', items[number]['title'])
                        message[request['request']] += 1
                        data_to_update.append(items[number])
                    else:
                        logger.debug('BREAK')
                        MySQLReq.record_response(request['request'], data_to_update)
                        breakflag = 1
                        break
                if breakflag:
                    break
                MySQLReq.record_response(request['request'], data_to_update)
                i += 1
                logger.debug('NEXT_PAGE')

        msg_title = '<p><b>Внимание, была обновлена информация по запросам: </b></p><p class="text-info">'

        # Считаем у кого сколько апдейтов накопилось
        logger.info(message)
        update_counter = 0
        for request in message:
            if message[request] > 0:
                msg_title = msg_title + request + '(' + str(message[request]) + '), '
                update_counter += 1

        # Если что-то апдейтили - шлем сообщение
        if update_counter > 0:
            msg_title = msg_title[:-2] + '</p>'
            logger.debug(msg_title)

            server.send_message_to_all(msg_title)
            msg_timeout = config.getint('renewer_settings', 'msg_appear_time')
            time.sleep(msg_timeout)
            server.send_message_to_all('')

        work_timeout = config.getint('renewer_settings', 'work_timeout')
        time.sleep(work_timeout)
    MySQLReq.connection.close()


if __name__ == "__main__":
    server_thread = threading.Thread(target=web_socket_msg)
    server_thread.start()

    msg_thread = threading.Thread(target=send_msg)
    msg_thread.start()
