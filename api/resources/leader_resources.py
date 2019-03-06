from django.db import IntegrityError
from django.utils.functional import cached_property

import api.rest as rest
from leader.models import LeaderPhoto


class Leader(rest.Resource):
    class Meta:
        path = '/api/leader/'

    id = rest.IntegerField()

    name = rest.TextField()

    phonenumber = rest.TextField(blank=True, null=True)

    email = rest.TextField()

    api_user = rest.ResourceField('apiauth.ApiUserResource')

    @cached_property
    def photo(self):
        leader_id = self.api_user
        if not isinstance(leader_id, int):
            leader_id = leader_id.id

        try:
            obj, created = LeaderPhoto.objects.get_or_create(leader_id=leader_id)

            return obj.photo

        except IntegrityError:
            return None


class Leaders(rest.ResourceCollection):
    class Meta:
        resource = Leader


class ChangeLeader(rest.Resource):
    class Meta:
        path = '/api/leader/change/'
        supported_operations = [rest.Operations.put]
        default_return_resource = Leader

    name = rest.TextField()

    phonenumber = rest.TextField()
