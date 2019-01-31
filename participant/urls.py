from django.urls import path

from participant.views import ClosedExperimentView, RegisterView

app_name = 'participant'

urlpatterns = [
    path('register/<int:experiment>/', RegisterView.as_view(), name='register'),
    path('closed/', ClosedExperimentView.as_view(), name='closed_experiment'),
]
