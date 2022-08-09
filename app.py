# -*- coding: utf-8 -*-
import multiprocessing

from flask import Flask, render_template
from multiprocessing import Process, Manager
from service.googlesheets_init import GoogleSheets
from service.db_operations import selectDataFromDB, updateTableDB, checkDateForExpiration
import time
import logs
# from threading import Thread, Lock


app = Flask(__name__)

def get_sheet(lock):
    """
        В этом процессе реализован периодический опрос документа Googlesheets и запись актуальных данных в БД PostgreSQL
        Процесс выполняется в режиме реального времени
    :param lock: экземпляр объекта блокировки процесса
    :return:
    """
    with GoogleSheets('creds.json', '1r4JlWmezNj_z1tbfQpf7MHSzU32Ju75zA_hsOcfrDlQ') as sheet:
        while True:
            logs.logger.debug('---Исполняется процесс 1---')
            value = sheet.getData()
            with lock:
                updateTableDB(value['values'])
            time.sleep(1)

def server(lock):
    """
        В это процессе реализована работа web-сервера Flask
    :param lock: экземпляр объекта блокировки процесса
    :return:
    """
    logs.logger.debug('---Исполняется процесс 2---')
    @app.route('/')
    def index():
        logs.logger.debug('---Обновлено окно index---')
        with lock:
            data = selectDataFromDB()
        return render_template('index.html', data=data)

    app.run(debug=True, host='0.0.0.0', port='5000')


def first_call(func):
    fl=False
    def wrapper():
        nonlocal fl
        if fl==False:
            func()
            fl=True
    return wrapper

@first_call
def notify_date_expired():
    """
        Отправка уведоления об истечении срока доставки
    :return:
    """
    checkDateForExpiration()


if __name__ == '__main__':

    lock = Manager().RLock()
    # lock = Lock()

    # notify_date_expired()

    procs = []
    procs.append(Process(target=server, args=(lock,)))
    procs.append(Process(target=get_sheet, args=(lock,)))
    # procs.append(Thread(target=server, args=(lock,)))
    # procs.append(Thread(target=get_sheet, args=(lock,)))


    for i,proc in enumerate(procs):
        logs.logger.debug('Запустился процесс {}'.format(i+1))
        proc.daemon = True
        proc.start()

    while True:
        pass
