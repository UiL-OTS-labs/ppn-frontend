from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from django.contrib.auth.views import LoginView

from api.resources import OpenExperiments, Admin
from main.mixins import OverrideLanguageMixin


class HomeView(OverrideLanguageMixin, generic.TemplateView):
    template_name = 'main/index.html'

    language_override = 'nl'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)

        experiments = OpenExperiments.client.get()
        admin = Admin.client.get()

        context['experiments'] = experiments
        context['admin'] = admin

        return context


class CustomLoginView(LoginView):

    def get_success_url(self):
        # HACK
        # Because we force the language to dutch on the frontpage, the language
        # can stay Dutch even if the logging in user has Accept-Language set to
        # english. This solves that problem.
        if '_language' in self.request.session:
            del self.request.session['_language']

        if self.request.user.is_leader():
            return reverse('leader:experiments')

        else:
            return reverse('main:home')


def handler404(request):
    return render(request, 'base/404.html', status=404)


def handler500(request):
    return render(request, 'base/500.html', status=500)
