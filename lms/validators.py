from rest_framework.serializers import ValidationError


class UrlValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        reg = 'https://www.youtube.com/'
        tmp_value = dict(value).get(self.field)
        if tmp_value is not None:
            if reg not in tmp_value:
                raise ValidationError('Недопустимый URL-адрес')
