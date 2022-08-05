from .models import Records
import datetime, time
from . import get_currency
from logs import logger
from service import tg, settings


def selectDataFromDB():
    logger.debug('---Вызвана фнукция selectDataFromDB---')
    data = []
    old_row=[]
    records = Records.select()
    for i, record in enumerate(records):
        row = [record.iid, record.order_id, record.cost_us, record.cost_rus, record.date]
        if i==0:
            data.append(row)
        if i>0 and row!=old_row:
            data.append(row)
        old_row = row
        logger.debug(row)
    logger.debug('---Конец чтения данных из БД---')
    return data


def updateTableDB(in_data):
    """
        Запись данных в БД
    :param in_data: данные, считанные из google sheet
    :return:
    """
    logger.debug('---Вызвана функция updateTableDB---')
        # обновляем курс доллара США на текущий день
    currentCourse = get_currency.getCourseUSD()
    logger.debug('---Курс доллара США на сегодня = {}---'.format(currentCourse))
        # полностью очищаем таблицу records перед записьмю
    Records.delete().execute()
        # сбрасываем индекс ключевого поля  таблицs records
    Records.truncate_table(restart_identity=True)
    for item in in_data:
        if all(item) and len(item) == 4:
            item = [x for x in map(lambda x: x.replace(',','.'), item)]
            iid=int(item[0])
            order_id=int(item[1])
            cost_us=float(item[2])
            cost_rus=round(float(item[2]).__mul__(currentCourse), 2)
            date=datetime.datetime.strptime(item[3], '%d.%m.%Y')
            logger.debug([iid, order_id,cost_us, cost_rus,date])
            record=Records(
                            iid=iid,
                            order_id=order_id,
                            cost_us=cost_us,
                            cost_rus=cost_rus,
                            date=date)
            record.save()
    logger.debug('---Конец записи данных в БД---')


def checkDateForExpiration():

    if settings.TG_BOT['TG_CHAT']!='' and settings.TG_BOT['TG_TOKEN']!='':
        current_date = datetime.datetime.now()
        timedelta = datetime.timedelta(days=1)

        old_row=[]
        records = Records.select()
        for i, record in enumerate(records):
            row = [record.iid, record.order_id, record.cost_us, record.cost_rus, record.date]
            if i==0:
                record_date = datetime.datetime.combine(record.date, datetime.time(hour=0, minute=0, second=0))
                if current_date - record_date > timedelta:
                    msg = 'Поставка по заказу № {} просрочена на {} дней'.format(row[1], \
                                                                                 (current_date - record_date))
                    tg.send_telegram(msg)
                    logger.debug(msg)

            if i>0 and row!=old_row:
                record_date = datetime.datetime.combine(record.date, datetime.time(hour=0, minute=0, second=0))
                if current_date - record_date > timedelta:
                    msg = 'Поставка по заказу № {} просрочена на {} дней'.format(row[1], \
                                                                                 (current_date - record_date))
                    tg.send_telegram(msg)
                    logger.debug(msg)

            old_row = row

        # Ветвь выполняется при первом вызове функции
    # if getattr(checkDateForExpiration,'old_date') is None:
    #     logger.debug('---Вызов функция checkDateForExpiration() при первом запуске приложения---')
    #     records = Records.select()
    #     for record in records:
    #         record.date = datetime.datetime.combine(record.date, datetime.time(hour=0,minute=0,second=0))
    #         if current_date - record.date > td:
    #             msg = 'Поставка по договору {} просрочена на {} дней'.format(record.order_id, \
    #                                                                          (current_date - record.date))
    #             tg.send_telegram(msg)
    #             logger.debug(msg)
    #     setattr(checkDateForExpiration,'old_date',current_date)
    # elif (current_date - getattr(checkDateForExpiration,'old_date')) > td:
    #     logger.debug('---Вызвана функция checkDateForExpiration()---')
    #     records = Records.select()
    #     for record in records:
    #         if current_date - record.date > td:
    #             msg = 'Поставка по договору {} просрочена на {} дней'.format(record.order_id, \
    #                                                                          (current_date - record.date))
    #             tg.send_telegram(msg)
    #             logger.debug(msg)
    #     setattr(checkDateForExpiration, 'old_date', current_date)
