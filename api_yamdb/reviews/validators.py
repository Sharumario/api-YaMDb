import datetime as dt

from django.forms import ValidationError


def validate_username_is_not_me(value):
    if value == 'me':
        raise ValidationError(
            'Использовать имя "me" запрещено',
            params={'value': value}
        )


def validate_year(value):
    year = dt.date.today().year
    if value > year:
        raise ValidationError(
            'Проверьте поле "year", оно не должно быть больше текущего!')
    return value
