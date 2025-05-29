""" Для поля описание определили пользовательский тип """

from sqlalchemy.types import TypeDecorator, Text
from src.value_objects.artist_description import Description


class DescriptionType(TypeDecorator):
    impl = Text
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is not None:
            # преобразуем объект Description в строку перед записью в базу данных
            return str(value)
        return None

    def process_result_value(self, value, dialect):
        if value is not None:
            # преобразуем строку из базы данных обратно в объект Description
            return Description(value)
        return None