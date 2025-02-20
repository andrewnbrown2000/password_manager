class Credential:
    def __init__(self, name, **fields):
        self.name = name
        for key, value in fields.items():
            setattr(self, key, value)