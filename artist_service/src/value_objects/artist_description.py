class Description:
    __value = str
    __limit_size = 1000

    def __init__(self, value: str):
        if len(value) > self.__limit_size:
            raise ValueError(f"Maximum description length is {self.__limit_size} characters")
        self.__value = value

    def __str__(self):
        return self.__value
