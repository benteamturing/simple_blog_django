from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q


class EmailModelBackend(ModelBackend):
    """
    email을 인증 수단으로 사용하는 인증
    django-admin은 email을 입력 받지만 username에 email을 저장
    client에서 api를 통해 생성한 계정은 email 필드에 email을 저장
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        email = kwargs.get('email', None)
        try:
            user = UserModel.objects.get(
                Q(email__iexact=username) |
                Q(email__iexact=email)
            )
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None
