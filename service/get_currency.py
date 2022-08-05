import service
import requests
import datetime
import xml.etree.ElementTree as ET
import xml.dom.minidom
from logs import logger

def updateCourse(func):
    """
        Обновление курса доллара производить либо при первом вызове функции getCourseUSD,
        либо не ранее чем, через сутки
    """
    def wrapper(*args):
            # day_start - начало рабочего времени в формате <YYYY-MM-DD 08:00:00>
        work_day_start = datetime.datetime.combine(datetime.date.today(), datetime.time(8, 0, 0))
        # work_day_start_ = datetime.datetime.combine(datetime.date.today(), datetime.time(8, 0, 10))
        if not hasattr(service,'firstCall'):
                # если это первый вызов функции после запуска приложения
            f = func(*args)
                # устанавливаем модулю service атрибут firstCall
            setattr(service,'firstCall',True)
            logger.debug('---Первый вызов функции getCourseUSD()---')
        # elif (datetime.datetime.now() > work_day_start) and \
        #         (datetime.datetime.now() < work_day_start_):
        elif (datetime.datetime.now() > work_day_start):
                # Если начались следующие сутки
            f = func(*args)
            logger.debug('---Однократный вызов функции getCourseUSD() в начале следующих суток---')
        else:
                # вернуть сохраненное значение
            f = getattr(service,'current_course')
            logger.debug('---Возврат сохраненного значения current_course---')
        return f
    return wrapper

@updateCourse
def getCourseUSD(date_str=None):
    """
        Парсинг текущего курса доллара США
        :res: - курс доллара на текущий день
    """
    date_str = datetime.datetime.now().strftime('%d/%m/%Y')  # конвертация текущей даты, пример 03/08/2022
    url = 'https://www.cbr.ru/scripts/XML_daily.asp?date_req='+ date_str

    responce = requests.get(url)

    def beautify_xml(xml_str):
        dom = xml.dom.minidom.parseString(xml_str)
        return dom.toprettyxml()

    # with open("currency.xml") as fin:
    #      data = fin.read()

    with open("currency.xml", "w") as fout:
        fout.write(beautify_xml(responce.text))

    tree = ET.parse('currency.xml').getroot().findall('Valute')
    [res] = [x.findtext('Value').replace(',','.') for x in tree if x.findtext('Name') == 'Доллар США']
    res=float(res)
        # сохранение даты последнего вызова функции
    setattr(service,'current_course',res)

    return res

if __name__ == '__main__':

    # print(datetime.datetime.now())
    # print(datetime.datetime.now()+datetime.timedelta(days=1))
    # print(getCourseUSD('03/08/2022'))
    # print(getCourseUSD('03/07/2022'))
    # print(getCourseUSD('03/06/2022'))
    print(getCourseUSD())