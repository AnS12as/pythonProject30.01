from rest_framework.exceptions import ValidationError
import re


def validate_youtube_url(value):
    youtube_regex = r'^https?://(www\.)?(youtube\.com|youtu\.be)/.+$'
    if not re.match(youtube_regex, value):
        raise ValidationError("Only YouTube links are allowed.")
