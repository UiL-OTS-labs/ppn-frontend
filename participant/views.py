from django.views import generic
from django.core.exceptions import ObjectDoesNotExist
from api.resources import Experiment


class RegisterView(generic.TemplateView):
    template_name = 'participant/register.html'

    def get_context_data(self, **kwargs):
        context = super(RegisterView, self).get_context_data(**kwargs)

        try:
            pk = self.kwargs.get('experiment')
            context['experiment'] = Experiment.client.get(pk=pk)
        except Exception as e:
            print(e)
            raise ObjectDoesNotExist

        return context
