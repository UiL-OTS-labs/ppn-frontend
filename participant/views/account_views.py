from django.contrib.auth import get_user_model
from django.views import generic

from api.auth.exceptions import AccountAlreadyExistsException
from api.resources import Admin
from main.mixins import OverrideLanguageMixin
from participant.forms import CreateAccountForm


class CreateAccountView(OverrideLanguageMixin, generic.FormView):
    template_name = 'participant/create_account.html'
    form_class = CreateAccountForm

    language_override = 'nl'

    status = 'ready'

    def form_valid(self, form):
        data = form.cleaned_data

        user_model = get_user_model()
        try:
            user_model.objects.create_user(**data)
        except AccountAlreadyExistsException:
            self.status = 'account_already_exists'
        else:
            self.status = 'account_created'

        return self.get(self.request)

    def get_context_data(self, **kwargs):
        context = super(CreateAccountView, self).get_context_data(
            **kwargs
        )

        context['admin'] = Admin.client.get()
        context['success'] = getattr(self, 'success', None)
        context['status'] = self.status

        return context
