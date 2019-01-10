from api.middleware import get_current_session
from .models import RemoteApiUser
from .resources import ApiUserResource
from ..exceptions import ApiError


class ApiAuthenticationBackend:

    def authenticate(self, request, username=None, password=None):
        if not username or not password:
            return None

        try:
            resource = ApiUserResource.client.get(username=username, password=password)
        except ApiError:
            return

        user = self._get_or_create_user(resource, username, request)

        return user

    def get_user(self, user_id):
        try:
            return RemoteApiUser.objects.get(pk=user_id)
        except RemoteApiUser.DoesNotExist:
            return None

    @staticmethod
    def _get_or_create_user(resource: ApiUserResource, username, request):
        try:
            user = RemoteApiUser.objects.get(pk=resource.pk)
        except RemoteApiUser.DoesNotExist:
            user = RemoteApiUser()
            user.pk = resource.pk
            user.email = username

        request.session['token'] = resource.token

        user.is_superuser = resource.is_admin
        user.is_staff = resource.is_admin
        user.is_active = resource.is_active
        user.save()

        return user
