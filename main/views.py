from django.shortcuts import render
from django.views import generic

from api.resources import OpenExperiments, Admin


class HomeView(generic.TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)

        experiments = OpenExperiments.client.get()
        admin = Admin.client.get()

        context['experiments'] = experiments
        context['admin'] = admin

        return context


def handler404(request):
    return render(request, 'base/404.html', status=404)


def handler500(request):
    return render(request, 'base/500.html', status=500)
