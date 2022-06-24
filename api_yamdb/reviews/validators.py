import datetime as dt
import re

from django.forms import ValidationError


def validate_username(value):
    if value == 'me':
        raise ValidationError('Использовать имя "me" запрещено')
    if not re.match(r'^[\w.@+-]+$', value):
        raise ValidationError(f'Псевдоним {value} содержит '
                              'недопустимые символы')
    return value


def validate_year(value):
    year = dt.date.today().year
    if value > year:
        raise ValidationError(
            f'Проверьте год ({year}), он не должен быть больше текущего')
    return value
