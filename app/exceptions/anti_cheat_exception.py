from app.exceptions.server_exception import ServerException


class AntiCheatException(ServerException):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

    def __repr__(self):
        return self.message
