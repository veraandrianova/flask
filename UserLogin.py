


class UserLogin:
    def fromDB(self, user_id, User):
        self.__user = User.query.get(user_id)
        print(self.__user, 'userloginfromdb')
        return self

    def create(self, user):
        self.__user = user
        return self

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        print(self.__user, 'get')
        return self.__user


