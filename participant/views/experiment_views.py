from braces import views as braces
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.functional import cached_property
from django.views import generic

from api.resources import Experiment
from api.resources.participant_resources import RequiredRegistrationFields
from main.mixins import OverrideLanguageMixin
from participant.forms import BaseRegisterForm
from participant.utils import get_register_form, submit_register_form, \
    get_authenticated_register_form


class ExperimentRegisterMixin:
    template_name = 'participant/register.html'
    language_override = 'nl'

    @cached_property
    def experiment(self):
        try:
            pk = self.kwargs.get('experiment')
            return Experiment.client.get(pk=pk)
        except Exception as e:
            raise ObjectDoesNotExist

    def get_context_data(self, **kwargs):
        context = super(ExperimentRegisterMixin, self).get_context_data(
            **kwargs)

        context['experiment'] = self.experiment

        return context


class RegisterView(OverrideLanguageMixin, ExperimentRegisterMixin,
                   generic.FormView):
    form_class = BaseRegisterForm
    language_override = 'nl'

    def __init__(self):
        super(RegisterView, self).__init__()
        self.success = None
        self.recoverable = None
        self.messages = []

    def get_context_data(self, **kwargs):
        context = super(RegisterView, self).get_context_data(**kwargs)

        context['success'] = self.success
        context['recoverable'] = self.recoverable
        context['api_messages'] = self.messages

        return context

    def dispatch(self, request, *args, **kwargs):
        try:
            # You might ask, why not just do the return in the body of this
            # if-statement. Well, that's because the very act of calling
            # self.experiment might raise ObjectDoesNotExist as well!
            # This way, we can do both in one except.
            if not self.experiment.open:
                raise ObjectDoesNotExist
        except ObjectDoesNotExist:
            return HttpResponseRedirect(
                reverse('participant:closed_experiment')
            )

        # If there's a participant logged in, redirect to the right version
        if request.user.is_authenticated and request.user.is_participant:
            args = [self.kwargs.get('experiment')]
            return HttpResponseRedirect(
                reverse('participant:register_logged_in', args=args)
            )

        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        base_form = super(RegisterView, self).get_form(form_class)

        return get_register_form(base_form, self.experiment)

    def form_valid(self, form):
        success, recoverable, messages =\
            submit_register_form(form, self.experiment)

        self.success = success
        self.recoverable = recoverable
        self.messages = messages
        return self.get(self.request, [], {})


class AuthenticatedRegisterView(braces.LoginRequiredMixin,
                                OverrideLanguageMixin,
                                ExperimentRegisterMixin,
                                generic.FormView):
    form_class = BaseRegisterForm

    def dispatch(self, request, *args, **kwargs):
        try:
            # You might ask, why not just do the return in the body of this
            # if-statement. Well, that's because the very act of calling
            # self.experiment might raise ObjectDoesNotExist as well!
            # This way, we can do both in one except.
            if not self.experiment.open:
                raise ObjectDoesNotExist
        except ObjectDoesNotExist:
            return HttpResponseRedirect(
                reverse('participant:closed_experiment')
            )

        # If there isn't a participant logged in, redirect to the right version
        if not request.user.is_participant:
            args = [self.kwargs.get('experiment')]
            return HttpResponseRedirect(
                reverse('participant:register', args=args)
            )

        return super(AuthenticatedRegisterView, self).dispatch(
            request,
            *args,
            **kwargs
        )

    def get_form(self, form_class=None):
        base_form = super(AuthenticatedRegisterView, self).get_form(form_class)

        fields = RequiredRegistrationFields.client.get(
            experiment=self.experiment.id
        ).fields

        return get_authenticated_register_form(
            base_form,
            self.experiment,
            fields
        )


class ClosedExperimentView(OverrideLanguageMixin, generic.TemplateView):
    template_name = 'participant/closed_experiment.html'
    language_override = 'nl'
