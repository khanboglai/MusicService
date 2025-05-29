

class DatabaseException(Exception):
    """ Исключение для отслеживания работы с бд (e.g. юзер ввел какую-то хрень) 423 """
    @property
    def message(self):
        return 'Database exception occured'
    

class DatabaseErrorException(Exception):
    """ Исключение для отслеживания ошибок работы бд (когда бд упала хрен пойми почему) 500 """
    @property
    def message(self):
        return 'Database error occured'
    