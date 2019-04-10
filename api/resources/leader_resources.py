from django.db import IntegrityError
from django.utils.functional import cached_property

import api.rest as rest
from leader.models import LeaderPhoto


#
# Leader resources
#

class Leader(rest.Resource):
    """
    Describes a leader, can be used to retrieve the current leader's profile
    or in other resources
    """

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
            obj, created = LeaderPhoto.objects.get_or_create(
                leader_id=leader_id)

            return obj.photo

        except IntegrityError:
            return None


class Leaders(rest.ResourceCollection):
    """
    A collection of leaders, used for the experiment's 'additional_leaders'
    field.
    """

    class Meta:
        resource = Leader


# TODO: maybe integrate this with the Leader resource?

class ChangeLeader(rest.Resource):
    """
    This resource is used to change a leader's profile
    """

    class Meta:
        path = '/api/leader/change/'
        supported_operations = [rest.Operations.put]
        default_return_resource = Leader

    name = rest.TextField()

    phonenumber = rest.TextField()
