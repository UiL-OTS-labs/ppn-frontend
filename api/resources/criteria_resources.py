import api.rest as rest


class DefaultCriteria(rest.Resource):

    id = rest.IntegerField()

    language = rest.TextField()

    multilingual = rest.TextField()

    sex = rest.TextField()

    handedness = rest.TextField()

    dyslexia = rest.TextField()

    social_status = rest.TextField()

    min_age = rest.IntegerField()

    max_age = rest.IntegerField()


class Criterion(rest.Resource):

    id = rest.IntegerField()

    name_form = rest.TextField()

    name_natural = rest.TextField()

    values = rest.TextField()

    @property
    def value_list(self):
        return self.values.split(',')


class ExperimentCriterion(rest.Resource):

    id = rest.IntegerField()

    criterion = rest.ResourceField(Criterion)

    correct_value = rest.TextField()

    message_failed = rest.TextField()


class ExperimentCriteria(rest.Collection):
    class Meta:
        resource = ExperimentCriterion
