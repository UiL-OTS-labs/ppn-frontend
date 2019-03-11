from braces import views as braces
from django.conf import settings
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied, SuspiciousOperation
from django.urls import reverse_lazy as reverse
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from django.views import generic

from api.auth.models import RemoteApiUser
from api.resources import ChangeLeader, Leader, LeaderExperiments, \
    SwitchExperimentOpen
from api.rest.exceptions import ApiError
from leader.forms import ChangeProfileForm, TimeSlotForm
from leader.models import LeaderPhoto
from leader.utils import add_timeslot, now, delete_timeslots, delete_timeslot
from main.mixins import ExperimentObjectMixin
from uil.core.views import RedirectActionView
from uil.core.views.mixins import RedirectSuccessMessageMixin


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


class TimeSlotHomeView(braces.LoginRequiredMixin,
                       ExperimentObjectMixin, generic.FormView):
    template_name = 'leader/timeslots.html'
    form_class = TimeSlotForm

    def post(self, request, *args, **kwargs):
        """This override ensures that we don't redirect after a successfull
        form POST. This is because we actually want to stay on the page and
        have access to the POST values.

        These post values are needed to fill in the datetime initial value.
        (People like it when the last filled in value is already filled in)
        """
        form = self.get_form()
        if form.is_valid():
            self.form_valid(form)
            return self.get(request, *args, **kwargs)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        """Only save the form, but stop there."""
        data = form.cleaned_data

        success = add_timeslot(data)

        if not success:
            messages.error(self.request, "There has been a problem when "
                                         "adding new slot(s). Please try again "
                                         "later.")
        else:
            messages.success(self.request, _('timeslots:message:added'))

        # Invalidate the self.experiment cache, causing a new fetch from the
        # backend. Otherwise the new slot won't appear until a refresh
        del self.experiment

    def get_initial(self):
        initial = super(TimeSlotHomeView, self).get_initial()

        initial['max_places'] = self.experiment.default_max_places
        initial['datetime'] = self._get_datetime_initial()
        initial['experiment'] = self.experiment.id

        return initial

    def _get_datetime_initial(self):
        """If we have post values, we return the datetime from POST,
        otherwise we default to now().
        """
        if self.request.POST:
            return self.request.POST['datetime']

        return str(now())[:-3]  # Remove the seconds

    def get_context_data(self, *_, **kwargs):
        context = super(TimeSlotHomeView, self).get_context_data(**kwargs)

        context['experiment'] = self.experiment

        return context


class TimeSlotDeleteView(braces.LoginRequiredMixin,
                         RedirectSuccessMessageMixin,
                         RedirectActionView):
    success_message = _('timeslots:message:deleted_timeslot')

    def action(self, request):
        timeslot_pk = self.kwargs.get('timeslot')
        experiment_pk = self.kwargs.get('experiment')

        delete_timeslot(experiment_pk, timeslot_pk)

    def get_redirect_url(self, *args, **kwargs):
        args = [self.kwargs.get('experiment')]
        return reverse('leader:timeslots', args=args)


class TimeSlotBulkDeleteView(braces.LoginRequiredMixin,
                             RedirectSuccessMessageMixin,
                             RedirectActionView):
    success_message = _('timeslots:message:deleted_timeslots')

    def action(self, request):
        if not request.method == 'POST':
            raise SuspiciousOperation

        experiment_pk = self.kwargs.get('experiment')

        delete_timeslots(experiment_pk, request.POST)

    def get_redirect_url(self, *args, **kwargs):
        args = [self.kwargs.get('experiment')]
        return reverse('leader:timeslots', args=args)


# class UnsubscribeParticipantView(braces.LoginRequiredMixin,
#                                  RedirectSuccessMessageMixin,
#                                  RedirectActionView):
#     success_message = _('timeslots:message:unsubscribed_participant')
#
#     def action(self, request):
#         appointment_pk = self.kwargs.get('appointment')
#
#         unsubscribe_participant(self.kwargs.get('time_slot'), appointment_pk)
#
#     def get_redirect_url(self, *args, **kwargs):
#         if self.request.GET.get('next'):
#             return self.request.GET.get('next')
#
#         return reverse(
#             'experiments:timeslots',
#             args=[self.time_slot.experiment.pk]
#         )
#
#     @cached_property
#     def time_slot(self):
#         return TimeSlot.objects.get(pk=)


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
            'name':  self.leader.name,
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
