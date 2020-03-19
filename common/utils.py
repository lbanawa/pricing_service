from passlib.hash import pbkdf2_sha512
import re


class Utils:
    @staticmethod
    # check if email has valid format
    def email_is_valid(email: str) -> bool:
        email_address_matcher = re.compile(r'^[\w-]+@([\w-]+\.)+[\w]+$') # jose-pricing@google.co.uk
        return True if email_address_matcher.match(email) else False

    # encrypt the password
    @staticmethod
    def hash_password(password: str) -> str:
        return pbkdf2_sha512.encrypt(password)

    # re-encrypt the password and compare the encrypted passwords to see if they match
    @staticmethod
    def check_hashed_password(password: str, hashed_password: str) -> bool:
        return pbkdf2_sha512.verify(password, hashed_password)