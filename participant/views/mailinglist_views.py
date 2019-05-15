from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.views import generic

from api.resources import Admin, MailinglistSubscribe
from api.resources.participant_resources import ValidateMailinglistToken, \
    UnsubscribeFromMailinglist
from api.rest import ApiError
from main.mixins import OverrideLanguageMixin
from participant.forms import SubscribeToMailinglistForm


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
        o.dyslexic = data.get('dyslexic')

        response = o.put()

        self.success = response.success

        return self.get(self.request)


class UnsubscribeFromMailinglistView(OverrideLanguageMixin,
                                     generic.TemplateView):
    template_name = 'participant/unsubscribe_mailinglist.html'
    language_override = 'nl'

    def get_context_data(self, **kwargs):
        context = super(UnsubscribeFromMailinglistView, self).get_context_data(
            **kwargs
        )

        context['token_valid'] = False
        context['email'] = None
        context['admin'] = Admin.client.get()

        try:
            validate = ValidateMailinglistToken()
            validate.token = self.kwargs.get('token', None)

            response = validate.put()

            context['token_valid'] = response.success
            context['email'] = response.email
        except ApiError:
            pass

        return context

    def post(self, request, token):
        unsub = UnsubscribeFromMailinglist()
        unsub.token = token
        unsub.put()

        messages.success(
            request,
            _('unsubscribe_mailinglist:messages:unsubscribed')
        )

        return HttpResponseRedirect(reverse('main:home'))
