from braces import views as braces
from django.conf import settings
from django.urls import reverse_lazy as reverse
from django.utils.functional import cached_property
from django.views import generic

from api.auth.models import RemoteApiUser
from api.resources import Leader, LeaderExperiments
from leader.forms import ChangeProfileForm
from leader.models import LeaderPhoto


class ExperimentsView(braces.RecentLoginRequiredMixin,
                      braces.GroupRequiredMixin,
                      generic.TemplateView):

    template_name = 'leader/experiments.html'
    group_required = [settings.GROUPS_LEADER]

    def get_context_data(self, **kwargs):
        context = super(ExperimentsView, self).get_context_data(**kwargs)

        context['experiments'] = LeaderExperiments.client.get()

        return context


class ProfileView(braces.RecentLoginRequiredMixin,
                  braces.GroupRequiredMixin,
                  generic.FormView):

    template_name = 'leader/profile.html'
    form_class = ChangeProfileForm
    success_url = reverse('leader:profile')
    group_required = [settings.GROUPS_LEADER]

    @cached_property
    def leader(self):
        return Leader.client.get()

    def get_initial(self):

        photo, created = LeaderPhoto.objects.get_or_create(
            leader=RemoteApiUser.objects.get(
                email=self.leader.email
            )
        )

        return {
            'name': self.leader.name,
            'email': self.leader.email,
            'phone': self.leader.phonenumber,
            'photo': photo.photo,
        }

    def form_valid(self, form):
        values = form.cleaned_data

        photo, created = LeaderPhoto.objects.get_or_create(
            leader=RemoteApiUser.objects.get(
                email=self.leader.email
            )
        )

        photo_val = values['photo'] or None  # This fixes a hilarious bug that
        # fills in 'False' when clearing the photo

        photo.photo = photo_val
        photo.save()

        return super(ProfileView, self).form_valid(form)
