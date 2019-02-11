from django.views import generic

from api.resources import  Admin, MailinglistSubscribe
from main.mixins import OverrideLanguageMixin
from participant.forms import  SubscribeToMailinglistForm


class SubscribeToMailinglistView(OverrideLanguageMixin, generic.FormView):
    template_name = 'participant/subscribe_mailinglist.html'
    language_override = 'nl'
    form_class = SubscribeToMailinglistForm

    def get_context_data(self, **kwargs):
        context = super(SubscribeToMailinglistView, self).get_context_data(
            **kwargs
        )

        context['admin'] = Admin.client.get()
        context['success'] = getattr(self, 'success', None)

        return context

    def form_valid(self, form):
        data = form.cleaned_data

        o = MailinglistSubscribe()
        o.email = data.get('email')
        o.language = data.get('language')
        o.multilingual = data.get('multilingual')
        o.dyslexic = data.get('dyslexic') == 'D'

        response = o.put()

        self.success = response.success

        return self.get(self.request)

