from . import models


class EmailAuthBackend(object):

    @staticmethod
    def authenticate(email=None, password=None):
        try:
            user = models.User.objects.get(email=email)
        except Exception:
            return None

        if not user.check_password(password):
            return None

        return user

    @staticmethod
    def get_user(user_id):
        try:
            return models.User.objects.get(pk=user_id)
        except Exception:
            return None