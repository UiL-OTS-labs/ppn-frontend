import api.rest as rest


class Leader(rest.Resource):
    class Meta:
        pass

    id = rest.IntegerField()

    name = rest.TextField()

    phonenumber = rest.TextField(blank=True, null=True)

    api_user = rest.IntegerField()


class Leaders(rest.Collection):
    class Meta:
        resource = Leader
