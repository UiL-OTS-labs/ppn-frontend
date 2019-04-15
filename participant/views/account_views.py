from django.contrib.auth import get_user_model
from django.views import generic

from api.resources import Admin
from main.mixins import OverrideLanguageMixin
from participant.forms import CreateAccountForm


class CreateAccountView(OverrideLanguageMixin, generic.FormView):
    template_name = 'participant/create_account.html'
    form_class = CreateAccountForm

    # TODO: add messages and a url to go to

    language_override = 'nl'

    def form_valid(self, form):
        data = form.cleaned_data

        user_model = get_user_model()
        user_model.objects.create_user(**data)

        return super(CreateAccountView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CreateAccountView, self).get_context_data(
            **kwargs
        )

        context['admin'] = Admin.client.get()
        context['success'] = getattr(self, 'success', None)

        return context
