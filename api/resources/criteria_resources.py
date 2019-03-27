from django.utils.translation import ugettext_lazy as _

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

    def get_language_display(self):
        if self.language == 'I':
            return _('globals:indifferent')

        return self.language

    def get_multilingual_display(self):
        if self.multilingual == 'I':
            return _('globals:indifferent')

        return self.multilingual

    def get_sex_display(self):
        if self.sex == 'I':
            return _('globals:indifferent')

        return self.sex

    def get_handedness_display(self):
        if self.handedness == 'I':
            return _('globals:indifferent')

        return self.handedness

    def get_social_status_display(self):
        if self.social_status == 'I':
            return _('globals:indifferent')

        return self.social_status

    def get_min_age_display(self):
        if self.min_age == -1:
            return _('globals:indifferent')

        return self.min_age

    def get_max_age_display(self):
        if self.max_age == -1:
            return _('globals:indifferent')

        return self.max_age


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


class ExperimentCriteria(rest.ResourceCollection):
    class Meta:
        resource = ExperimentCriterion
