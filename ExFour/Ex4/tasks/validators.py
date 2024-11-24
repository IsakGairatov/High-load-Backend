import magic
from rest_framework.exceptions import ValidationError


def validate_file_type(file):
    mime = magic.Magic(mime=True)
    file_type = mime.from_buffer(file.read())
    allowed_types = ['text/csv', 'application/pdf']
    if file_type not in allowed_types:
        raise ValidationError("Invalid file type")

