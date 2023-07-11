from app.exceptions.server_exception import ServerException


class UserBannedException(ServerException):
    def __init__(self, user: str):
        super().__init__(f'User {user} is banned!')
