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

    defaultcriteria = rest.ResourceField('DefaultCriteria')

    specific_criteria = rest.CollectionField('ExperimentCriteria')

    timeslots = rest.CollectionField('TimeSlots')

    def n_timeslots(self):
        return sum([x.max_places for x in self.timeslots])

    def display_additional_leaders(self):
        return ",".join([leader.name for leader in self.additional_leaders])


class SwitchExperimentOpen(rest.Resource):
    class Meta:
        path = '/api/experiment/{experiment}/switch_open/'
        supported_operations = [rest.Operations.get_over_post]
        path_variables = ['experiment']

    success = rest.BoolField()

    open = rest.BoolField()


class LeaderExperiments(rest.ResourceCollection):
    class Meta:
        resource = Experiment
        path = '/api/leader_experiments/'


class OpenExperiments(rest.ResourceCollection):
    class Meta:
        resource = Experiment
        path = '/api/experiments/'


class RegistrationCriterion(rest.Resource):

    name = rest.TextField()

    value = rest.TextField()


class RegistrationCriteria(rest.ResourceCollection):
    class Meta:
        resource = RegistrationCriterion


class ExperimentRegistrationResponse(rest.Resource):

    success = rest.BoolField()

    recoverable = rest.BoolField()

    messages = rest.CollectionField(rest.StringCollection)


class ExperimentRegistration(rest.Resource):
    class Meta:
        path = '/api/experiment/{experiment}/register/'
        supported_operations = [rest.Operations.put]
        path_variables = ['experiment']
        default_return_resource = ExperimentRegistrationResponse

    name = rest.TextField(
        blank=True,
        null=True,
    )

    email = rest.TextField(
        blank=True,
        null=True,
    )

    phone = rest.TextField(
        blank=True,
        null=True,
    )

    birth_date = rest.DateField(
        blank=True,
        null=True,
    )

    multilingual = rest.TextField(
        blank=True,
        null=True,
    )

    language = rest.TextField(
        blank=True,
        null=True,
    )

    sex = rest.TextField(
        blank=True,
        null=True,
    )

    handedness = rest.TextField(
        blank=True,
        null=True,
    )

    dyslexic = rest.TextField(
        blank=True,
        null=True,
    )

    social_status = rest.TextField(
        blank=True,
        null=True,
    )

    specific_criteria = rest.CollectionField(
        RegistrationCriteria
    )

    timeslot = rest.IntegerField()

    mailinglist = rest.BoolField(
        default=False
    )
