from django.urls import path

from .views import ExperimentsView, ProfileView, SwitchExperimentOpenView, \
    TimeSlotHomeView, TimeSlotDeleteView, TimeSlotBulkDeleteView

app_name = 'leader'

urlpatterns = [
    path('', ExperimentsView.as_view(), name='experiments'),
    path('experiment/<int:experiment>/switch_open',
         SwitchExperimentOpenView.as_view(), name='experiment_switch_open'),
    path('experiment/<int:experiment>/timeslots/',
         TimeSlotHomeView.as_view(), name='timeslots',
    ),

    path('experiment/<int:experiment>/timeslots/<int:timeslot>/delete/',
         TimeSlotDeleteView.as_view(), name='delete_timeslot'),

    path('experiment/<int:experiment>/timeslots/delete/',
         TimeSlotBulkDeleteView.as_view(), name='delete_timeslots'),


    path('profile/', ProfileView.as_view(), name='profile'),
]
