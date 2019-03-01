from braces import views as braces
from django.conf import settings
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy as reverse
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from django.views import generic
from uil.core.views import RedirectActionView
from uil.core.views.mixins import RedirectSuccessMessageMixin

from api.auth.models import RemoteApiUser
from api.exceptions import ApiError
from api.resources import Leader, LeaderExperiments, SwitchExperimentOpen, \
    ChangeLeader
from leader.forms import ChangeProfileForm
from leader.models import LeaderPhoto


class ExperimentsView(braces.LoginRequiredMixin,
                      braces.GroupRequiredMixin,
                      generic.TemplateView):

    template_name = 'leader/experiments.html'
    group_required = [settings.GROUPS_LEADER]

    def get_context_data(self, **kwargs):
        context = super(ExperimentsView, self).get_context_data(**kwargs)

        context['experiments'] = LeaderExperiments.client.get()

        return context


class SwitchExperimentOpenView(braces.RecentLoginRequiredMixin,
                               braces.GroupRequiredMixin,
                               RedirectSuccessMessageMixin,
                               RedirectActionView):
    group_required = [settings.GROUPS_LEADER]
    pattern_name = 'leader:experiments'

    def get_redirect_url(self, *args, **kwargs):
        return reverse(self.pattern_name)

    def action(self, request):
        experiment = self.kwargs.pop('experiment')

        try:
            res = SwitchExperimentOpen.client.get(experiment=experiment)

            if res.success:
                if res.open:
                    self.success_message = _('experiment:message:open')
                else:
                    self.success_message = _('experiment:message:closed')
            else:
                self.success_message = _('experiment:message:fail')

        except ApiError as e:
            if e.status_code == 403:
                raise PermissionDenied

            self.success_message = _('experiment:message:fail')


class ProfileView(braces.RecentLoginRequiredMixin,
                  braces.GroupRequiredMixin,
                  SuccessMessageMixin,
                  generic.FormView):

    template_name = 'leader/profile.html'
    form_class = ChangeProfileForm
    success_url = reverse('leader:experiments')
    success_message = _('profile:message:updated')
    group_required = [settings.GROUPS_LEADER]

    @cached_property
    def leader(self):
        return Leader.client.get()

    def get_initial(self):

        photo, created = LeaderPhoto.objects.get_or_create(
            leader=RemoteApiUser.objects.get_by_email(
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
            leader=RemoteApiUser.objects.get_by_email(
                email=self.leader.email
            )
        )

        photo_val = values['photo'] or None  # This fixes a hilarious bug that
        # fills in 'False' when clearing the photo

        photo.photo = photo_val
        photo.save()

        change_leader = ChangeLeader()
        change_leader.name = values['name']
        change_leader.phonenumber = values['phone']
        change_leader.put()

        return super(ProfileView, self).form_valid(form)
