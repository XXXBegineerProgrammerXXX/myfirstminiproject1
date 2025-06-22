from django.core.exceptions import ValidationError
import re

def validate_password(value):
    if not re.search('^[a-zA-Z0-9 _]*$', value):
        raise ValidationError('Пароль может содержать только цифры, английские буквы, пробелы и нижнее подчеркивание')
    elif not re.search(r'[0-9]', value):
        raise ValidationError('Пароль должен содержать хотя бы одну цифру!')
    elif len(value) < 6 or len(value) > 32:
        raise ValidationError('Длина пароля должна быть от 6 до 32 символов!')