import uuid


class IdGenerator:

    @staticmethod
    def generateId():
        return uuid.uuid1().hex
