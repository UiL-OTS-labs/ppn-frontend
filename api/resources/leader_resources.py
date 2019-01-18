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

        obj, created = LeaderPhoto.objects.get_or_create(leader_id=leader_id)

        return obj.photo


class Leaders(rest.Collection):
    class Meta:
        resource = Leader
