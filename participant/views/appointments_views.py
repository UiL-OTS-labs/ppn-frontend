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
