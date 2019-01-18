from django.urls import path

from .views import ExperimentsView, ProfileView, SwitchExperimentOpenView


app_name = 'leader'

urlpatterns = [
    path('', ExperimentsView.as_view(), name='experiments'),
    path('experiment/<int:experiment>/switch_open',
         SwitchExperimentOpenView.as_view(), name='experiment_switch_open'),
    path('profile/', ProfileView.as_view(), name='profile'),
]
