from django.contrib.auth import get_user_model
from django.contrib.messages import error
from django.views import generic

from api.auth.exceptions import AccountAlreadyExistsException
from api.resources import Admin, MailinglistSubscribe
from main.mixins import OverrideLanguageMixin
from participant.forms import SignUpForm


class SignUpView(OverrideLanguageMixin, generic.FormView):
    template_name = 'participant/sign_up.html'
    form_class = SignUpForm

    language_override = 'nl'

    status = 'ready'

    def form_invalid(self, form):
        # Use messages to show the error in an error-box, as the form won't
        # render it properly because this question is manually rendered
        if 'account' in form.errors:
            error(self.request, form.errors['account'][0])

        return super().form_invalid(form)

    def form_valid(self, form):
        data = form.cleaned_data

        if data.get('account'):
            self._handle_account(data)
        else:
            self._handle_mailing_list(data)

        return self.get(self.request)

    def _handle_account(self, data):
        user_model = get_user_model()
        try:
            user_model.objects.create_user(**data)
        except AccountAlreadyExistsException:
            error(
                self.request,
                "Het door jou opgegeven e-mail adres is al in gebruik!"
            )
        else:
            self.status = 'account_created'

    def _handle_mailing_list(self, data):
        o = MailinglistSubscribe()
        o.email = data.get('email')
        o.language = data.get('language')
        o.multilingual = data.get('multilingual')
        o.dyslexic = data.get('dyslexic')

        response = o.put()

        if response.success:
            self.status = "subscribed"
        else:
            error(
                self.request,
                "Het door jou opgegeven e-mail adres is al in gebruik!"
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(
            **kwargs
        )

        context['admin'] = Admin.client.get()
        context['status'] = self.status

        return context
