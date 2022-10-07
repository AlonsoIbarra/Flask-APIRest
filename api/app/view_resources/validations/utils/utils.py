import re
import datetime


def birthdate_validation():
    def validate(data):
        try:
            datetime.datetime.strptime(data, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Incorrect data format, should be YYYY-MM-DD")
        return data
    return validate


def email_validation():
    def validate(data):
        regex = re.compile(
            r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
        )
        if not re.fullmatch(regex, data):
            raise ValueError("Incorrect email format")
        return data
    return validate


def phone_validation(length):
    def validate(data):
        if data.isupper() or data.islower():
            raise ValueError(
                "Phone number must not contains letters"
            )
        if len(data) > length:
            raise ValueError(
                "Phone number must be a maximun of %i characters long" % length
            )
        return data
    return validate


def postal_code_validation(length):
    def validate(data):
        if data.isupper() or data.islower():
            raise ValueError(
                "Postal code must be numbers"
            )
        if len(data) > length:
            raise ValueError(
                "Postal code must be a maximun of %i characters long" % length
            )
        return data
    return validate
