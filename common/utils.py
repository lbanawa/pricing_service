import re


class Utils:
    @staticmethod
    # check if email has valid format
    def email_is_valid(email: str) -> bool:
        email_address_matcher = re.compile(r'^[\w-]+@([\w-]+\.)+[\w]+$') # jose-pricing@google.co.uk
        return True if email_address_matcher.match(email) else False
