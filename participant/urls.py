from django.urls import path

from participant.views import ClosedExperimentView, RegisterView, \
    SubscribeToMailinglistView

app_name = 'participant'

urlpatterns = [
    path('register/<int:experiment>/', RegisterView.as_view(), name='register'),
    path('closed/', ClosedExperimentView.as_view(), name='closed_experiment'),
    path('subscribe/', SubscribeToMailinglistView.as_view(), name='subscribe'),
]
