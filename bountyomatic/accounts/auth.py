from .models import User


class BasicBackend:
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


class EmailBackend(BasicBackend):
    def authenticate(self, username=None, password=None):
        # If username is an email address, then try to pull it up
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            user = None
        if not user:
            # We have a non-email address username we should try username
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = None
        if user and user.check_password(password):
            return user
