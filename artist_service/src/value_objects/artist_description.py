class Description:
    LIMIT_SIZE = 1000

    def __init__(self, value: str):
        if len(value) > self.LIMIT_SIZE:
            raise ValueError(f"Maximum description length is {self.LIMIT_SIZE} characters")
        self.value = value

    def __str__(self):
        return self.value


    def __composite_values__(self):
        return (self.value,)
