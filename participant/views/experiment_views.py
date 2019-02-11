from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.functional import cached_property
from django.views import generic

from api.resources import Experiment, Appointments
from main.mixins import OverrideLanguageMixin
from participant.forms import BaseRegisterForm
from participant.utils import get_register_form, submit_register_form


class RegisterView(OverrideLanguageMixin, generic.FormView):
    template_name = 'participant/register.html'
    language_override = 'nl'
    form_class = BaseRegisterForm

    def dispatch(self, request, *args, **kwargs):
        if not self.experiment.open:
            return HttpResponseRedirect(
                reverse('participant:closed_experiment')
            )

        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        base_form = super(RegisterView, self).get_form(form_class)

        return get_register_form(base_form, self.experiment)

    def form_valid(self, form):
        submit_register_form(form)
        return HttpResponseRedirect(self.get_success_url())

    @cached_property
    def experiment(self):
        try:
            pk = self.kwargs.get('experiment')
            return Experiment.client.get(pk=pk)
        except Exception as e:
            print(e)
            raise ObjectDoesNotExist

    def get_context_data(self, **kwargs):
        context = super(RegisterView, self).get_context_data(**kwargs)

        context['experiment'] = self.experiment

        return context


class ClosedExperimentView(OverrideLanguageMixin, generic.TemplateView):
    template_name = 'participant/closed_experiment.html'
    language_override = 'nl'


class MyAppointmentsView(OverrideLanguageMixin, generic.TemplateView):
    template_name = 'participant/appointments/appointments.html'
    language_override = 'nl'

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and not user.is_participant:
            return HttpResponseRedirect(reverse('main:login'))

        return super(MyAppointmentsView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(MyAppointmentsView, self).get_context_data(**kwargs)

        context['appointments'] = Appointments.client.get()

        return context
