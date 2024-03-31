from model.user import User


class Post:
    def __init__(self, id, body, user: User):
        self.body = body
        self.user = user
        self.id = id
