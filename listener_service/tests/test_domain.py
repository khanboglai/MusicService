import pytest
from datetime import date, timedelta
from app.domain.entities.real.listener import Listener
from app.domain.values.real.name import Name
from app.domain.values.real.age import Age
from app.domain.exceptions.real.age import (
    AgeIncorrectFormat,
    AgeTooBigException,
    AgeTooSmallException,
)
from app.domain.values.abc.base import BaseValueObject
from app.domain.exceptions.real.names import (
    NameTooLongException,
    EmptyNameException,
    NotRealNameException
)

class TestBaseValueObject:
    """Тесты базового класса BaseValueObject"""

    def test_skip_validation(self):
        """Тест пропуска валидации"""
        class TestValueObject(BaseValueObject):
            def validate(self):
                raise ValueError("Validation should be skipped")
        
        # Не должно вызывать исключение при skip_validation=True
        obj = TestValueObject("test", skip_validation=True)
        assert obj.value == "test"

    def test_value_assignment(self):
        """Тест присвоения значения"""
        class TestValueObject(BaseValueObject):
            def validate(self):
                pass
        
        obj = TestValueObject("test_value")
        assert obj.value == "test_value"

class TestNameValidation:
    """Тесты валидации имени"""
    
    # Позитивные тесты
    @pytest.mark.parametrize("valid_name", [
        "Иван",
        "Anna",
        "Ёжиков",
        "A" * 20,  # Максимальная длина
    ])
    def test_valid_names(self, valid_name):
        """Тест корректных имен"""
        name = Name(valid_name)
        assert name.value == valid_name

    @pytest.mark.parametrize("empty_name,exception", [
        ("", EmptyNameException),
        ("   ", EmptyNameException),
    ])
    def test_empty_names(self, empty_name, exception):
        """Тест пустых имен"""
        with pytest.raises(exception):
            Name(empty_name)

    def test_none_name(self):
        """Тест None значения"""
        with pytest.raises(TypeError):
            Name(None)

    # Тесты на длину имени
    def test_name_too_long(self):
        """Тест слишком длинного имени"""
        with pytest.raises(NameTooLongException):
            Name("A" * 21)

    # Тесты на недопустимые символы
    @pytest.mark.parametrize("invalid_name", [
        "Иван123",
        "Ivan!",
        "John_Doe",
        "Иван Петров",
        "<script>",
        "Иван\nПетров",
    ])
    def test_invalid_characters(self, invalid_name):
        """Тест недопустимых символов"""
        with pytest.raises(NotRealNameException):
            Name(invalid_name)

    # Тест skip_validation
    def test_name_skip_validation(self):
        """Тест пропуска валидации"""
        invalid_name = "Invalid123!"
        name = Name(invalid_name, skip_validation=True)
        assert name.value == invalid_name

    # Тест на наследование от BaseValueObject
    def test_inheritance(self):
        """Проверка наследования"""
        assert issubclass(Name, BaseValueObject)
        assert hasattr(Name, 'validate')
        assert Name.validate.__isabstractmethod__ is False

    # Тест на строковое представление
    def test_str_representation(self):
        """Тест строкового представления"""
        name = Name("Иван")
        assert str(name) == "Иван"
        assert repr(name) == "Name('Иван')"

# --- Тесты для класса Age ---
@pytest.mark.parametrize("age_value,expected_exception,description", [
    # Неправильный формат
    (None, AgeIncorrectFormat, "None дата"),
    ("", AgeIncorrectFormat, "Пустая строка"),
    ("   ", AgeIncorrectFormat, "Пробелы"),
    ("01-01-2000", AgeIncorrectFormat, "Неправильный разделитель"),
    ("32.13.2000", AgeIncorrectFormat, "Несуществующая дата"),
    
    # Недопустимый возраст
    (date.today().strftime("%d.%m.%Y"), AgeTooSmallException, "Сегодняшняя дата"),
    ((date.today() + timedelta(days=1)).strftime("%d.%m.%Y"), AgeTooSmallException, "Дата в будущем"),
    ("01.01.1000", AgeTooBigException, "Слишком старая дата"),
])
def test_age_validation(age_value, expected_exception, description):
    with pytest.raises(expected_exception):
        Age(age_value)

# --- Тесты для класса Listener ---
@pytest.mark.parametrize("user_id,firstname,lastname,birthdate,expected_exception,description", [
    # Невалидные user_id
    (None, "Иван", "Иванов", "01.01.1990", TypeError, "None user_id"),
    (0, "Иван", "Иванов", "01.01.1990", ValueError, "user_id = 0"),
    (-1, "Иван", "Иванов", "01.01.1990", ValueError, "Отрицательный user_id"),
    
    # Невалидные имена
    (1, None, "Иванов", "01.01.1990", EmptyNameException, "None имя"),
    (1, "", "Иванов", "01.01.1990", EmptyNameException, "Пустое имя"),
    (1, "Иван", "Иванов123", "01.01.1990", NotRealNameException, "Цифры в фамилии"),
    
    # Невалидные даты
    (1, "Иван", "Иванов", None, AgeIncorrectFormat, "None дата"),
    (1, "Иван", "Иванов", "01/01/1990", AgeIncorrectFormat, "Неправильный формат даты"),
    (1, "Иван", "Иванов", "01.01.3000", AgeTooSmallException, "Дата в будущем"),
])
def test_listener_validation(user_id, firstname, lastname, birthdate, expected_exception, description):
    with pytest.raises(expected_exception):
        Listener(
            user_id=user_id,
            firstname=Name(firstname) if isinstance(firstname, str) else firstname,
            lastname=Name(lastname) if isinstance(lastname, str) else lastname,
            birthdate=Age(birthdate) if isinstance(birthdate, str) else birthdate
        )

# --- Позитивные тесты ---
@pytest.mark.parametrize("firstname,lastname,birthdate", [
    ("Иван", "Иванов", "01.01.1990"),
    ("Анна-Мария", "Петрова-Смирнова", "15.05.1985"),
    ("John", "Doe", "31.12.2000"),
])
def test_valid_listener_creation(firstname, lastname, birthdate):
    listener = Listener(
        user_id=1,
        firstname=Name(firstname),
        lastname=Name(lastname),
        birthdate=Age(birthdate)
    )
    assert listener.user_id == 1
    assert str(listener.firstname) == firstname
    assert str(listener.lastname) == lastname
    assert listener.birthdate.value == birthdate