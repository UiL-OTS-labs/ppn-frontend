from api.client import client
from .models import RemoteApiUser


class ApiAuthenticationBackend:

    def __init__(self):
        self._client = client

    def authenticate(self, request, username=None, password=None):
        if not username or not password:
            return None

        user = None
        # TODO: move all request code to a client service
        request = self._client.post('/api/auth/', {
            'password': password,
            'username': username
        })

        if request.ok:
            json = request.json()
            user = self._get_or_create_user(json, username)

        return user

    def get_user(self, user_id):
        try:
            return RemoteApiUser.objects.get(pk=user_id)
        except RemoteApiUser.DoesNotExist:
            return None

    def _get_or_create_user(self, json, username):
        try:
            user = RemoteApiUser.objects.get(pk=json['pk'])
        except RemoteApiUser.DoesNotExist:
            user = RemoteApiUser()
            user.pk = json['pk']
            user.email = username

        user.token = json['token']
        user.is_superuser = json['is_admin']
        user.is_staff = json['is_admin']
        user.is_active = json['is_active']

        user.save()

        return user
