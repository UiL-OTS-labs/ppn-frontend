from django.views import generic

from api.resources import LeaderExperiments


class ExperimentsView(generic.TemplateView):
    template_name = 'leader/experiments.html'

    def get_context_data(self, **kwargs):
        context = super(ExperimentsView, self).get_context_data(**kwargs)

        context['experiments'] = LeaderExperiments.client.get()

        return context
