import re

from rest_framework import serializers


def validate_username(value):
    if value == 'me':
        raise serializers.ValidationError('Использовать имя "me" '
                                          'запрещено')
    if not re.match(r'^[\w.@+-]+$', value):
        raise serializers.ValidationError(f'Псевдоним {value} содержит '
                                          'недопустимые символы')
    return value
