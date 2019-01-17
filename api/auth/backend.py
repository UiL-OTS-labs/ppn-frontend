from django.contrib.auth.models import Group

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
        if resource is None:
            return None

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

        existing_groups = list(user.groups.all())

        for group in resource.groups:
            o, created = Group.objects.get_or_create(
                name=group.name,
                pk=group.pk
            )

            if o in existing_groups:
                # If we have a group that's already registered, remove it
                # from the existing list
                existing_groups.remove(o)
            else:
                user.groups.add(o)

        for group in existing_groups:
            # Loop over the existing list, and remove all that are still in
            # the list
            # Any group that's still in the list are not in the API anymore,
            # so we should revoke their membership here too.
            user.groups.remove(group)

        user.save()

        return user
