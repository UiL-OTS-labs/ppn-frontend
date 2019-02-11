from django.urls import include, path

from participant.views import CancelLandingView, ClosedExperimentView, \
    MyAppointmentsView, RegisterView, SubscribeToMailinglistView

app_name = 'participant'

urlpatterns = [
    path('register/<int:experiment>/', RegisterView.as_view(), name='register'),
    path('closed/', ClosedExperimentView.as_view(), name='closed_experiment'),
    path('subscribe/', SubscribeToMailinglistView.as_view(), name='subscribe'),
    path('cancel/', include([
        path('', CancelLandingView.as_view(), name='cancel_landing'),
    ])),
    path('appointments/', MyAppointmentsView.as_view(), name='appointments'),
]
