class Flask:
    def __init__(self):
        self.name = self.__name__

    def __str__(self):
        return self.name
