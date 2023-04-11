import random
import string

import six
from django.contrib.auth.tokens import PasswordResetTokenGenerator
# from django.core.exceptions import ValidationError
from django.utils.text import slugify


# def validate_media(file):
#     """
#         Check if image length is greater than 5 Mb
#     """
#     file_size = file.size
#     limit_mb = 5
#     if file_size > limit_mb * 1024 * 1024:
#         raise ValidationError("La taille maximal autorisée est de %s MB" % limit_mb)

# def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
#     """
#         Generate a random string
#         return String (ascii && lowercase)
#     """
#     return ''.join(random.choice(chars) for _ in range(size))

def unique_user_slug_generator(instance, new_slug=None):
    """
        Unique slug generator with model username field
        return String
    """
    return slugify(instance.username)


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )

account_activation_token = TokenGenerator()