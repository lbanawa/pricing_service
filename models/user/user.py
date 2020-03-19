import uuid
from dataclasses import dataclass, field
from typing import Dict

from models.model import Model
from common.utils import Utils
import models.user.errors as UserErrors


@dataclass
class User(Model):
    collection: str = field(init=False, default='users')
    email: str
    password: str
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)

    @classmethod
    def find_by_email(cls, email: str) -> "User":
        try:
            return cls.find_one_by('email', email)
        except TypeError:
            # raise one of these custom errors when we cannot find the user in the database
            raise UserErrors.UserNotFoundError('A user with this e-mail was not found.')

    @classmethod
    def is_login_valid(cls, email: str, password: str) -> bool:
        # check if user exists -- if so, continue
        user = cls.find_by_email(email)

        # check if the encrypted/ hashed passwords match -- if not, give message that password was incorrect
        if not Utils.check_hashed_password(password, user.password):
            raise UserErrors.IncorrectPasswordError('Your password was incorrect.')

        return True

    @classmethod
    def register_user(cls, email: str, password: str) -> bool:
        # check that email is in correct format -- return invalid email error if not
        if not Utils.email_is_valid(email):
            raise UserErrors.InvalidEmailError('The e-mail does not have the correct format.')

        # if it is in the correct format, check if user already exists -- if so return error saying that user already exists
        try:
            cls.find_by_email(email)
            raise UserErrors.UserAlreadyRegisteredError('The e-mail you used to register already exists.')
        # if the user does not exist, make a new one
        except UserErrors.UserNotFoundError:
            User(email, Utils.hash_password(password)).save_to_mongo()

        return True

    # return all of the properties of the user -- does not share publicly, only in database
    def json(self) -> Dict:
        return {
            '_id': self._id,
            'email': self.email,
            'password': self.password
        }
