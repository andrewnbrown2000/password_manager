class Credential:
    def __init__(self, credential_name, **fields):
        self.credential_name = credential_name
        for key, value in fields.items():
            setattr(self, key, value)
    
    def names_only(self):
        return {"credential_name": self.credential_name}