from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from main.mixins import OverrideLanguageMixin


class CancelLandingView(OverrideLanguageMixin, generic.TemplateView):
    template_name = 'participant/appointments/cancel_landing.html'
    language_override = 'nl'

    def get(self, request, *args, **kwargs):
        # Redirect to 'My appointments' if a participant is logged in.
        if request.user.is_authenticated and request.user.is_participant:
            return HttpResponseRedirect(reverse('participant:appointments'))

        return super(CancelLandingView, self).get(request, *args, **kwargs)


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
