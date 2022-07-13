import uuid


class IdGenerator:
    @staticmethod
    def generateId() -> str:
        """
        Generates a unique ID.
        Something like: "cf470cf5dbd411ecad15001986003168"
        """
        return uuid.uuid1().hex
