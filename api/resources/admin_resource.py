import api.rest as rest


class Admin(rest.Resource):
    class Meta:
        path = '/api/admin/'
        identifier_field = 'email'

    first_name = rest.TextField()

    last_name = rest.TextField()

    email = rest.TextField()

    @property
    def name(self):
        return "{} {}".format(self.first_name, self.last_name)
