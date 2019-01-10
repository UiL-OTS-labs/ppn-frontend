import api.rest as rest


class Location(rest.Resource):

    id = rest.IntegerField()

    name = rest.TextField()

    route_url = rest.TextField(blank=True, null=True)


class Experiment(rest.Resource):
    class Meta:
        path = '/api/experiments/{pk}/'
        path_variables = ['pk']

    id = rest.IntegerField()

    name = rest.TextField()

    duration = rest.TextField()

    compensation = rest.TextField()

    task_description = rest.TextField(blank=True)

    additional_instructions = rest.TextField(blank=True)

    open = rest.BoolField()

    public = rest.BoolField()

    participants_visible = rest.BoolField()

    location = rest.ResourceField(Location)

    leader = rest.ResourceField('Leader')  # We cannot import this, as this
    # will cause a circular import

    additional_leaders = rest.CollectionField('Leaders')

    excluded_experiments = rest.CollectionField('OpenExperiments')

    def display_additional_leaders(self):
        return ",".join([leader.name for leader in self.additional_leaders])


class OpenExperiments(rest.Collection):
    class Meta:
        resource = Experiment
        path = '/api/experiments/'
