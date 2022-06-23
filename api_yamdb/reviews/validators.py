from django.forms import ValidationError


def validate_username_is_not_me(value):
    if value == 'me':
        raise ValidationError(
            'Использовать имя "me" запрещено',
            params={'value': value}
        )
