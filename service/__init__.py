from service.db_operations import checkDateForExpiration

    # установить аттрибут для функции checkDateForExpiration()
    # аттрибут old_date используется для сохранения даты последнего уведомления о просроке даты доставки
setattr(checkDateForExpiration,'old_date', None)