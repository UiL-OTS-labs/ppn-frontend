from django.urls import include, path

from participant.views import AuthenticatedRegisterView, CancelAppointmentView, \
    CancelLandingView, ClosedExperimentView, MyAppointmentsView, RegisterView, \
    SubscribeToMailinglistView

app_name = 'participant'

urlpatterns = [
    path('register/<int:experiment>/', RegisterView.as_view(), name='register'),
    path(
        'secure/register/<int:experiment>/',
        AuthenticatedRegisterView.as_view(),
        name='register_logged_in'
    ),

    path('closed/', ClosedExperimentView.as_view(), name='closed_experiment'),
    path('subscribe/', SubscribeToMailinglistView.as_view(), name='subscribe'),
    path('cancel/', include([
        path('', CancelLandingView.as_view(), name='cancel_landing'),
    ])),

    path('appointments/', MyAppointmentsView.as_view(), name='appointments'),
    path(
        'appointments/<str:token>/',
        MyAppointmentsView.as_view(),
        name='appointments'
    ),
    path(
        'appointments/<int:appointment>/cancel/',
        CancelAppointmentView.as_view(),
        name='cancel_appointment'
    ),
    path(
        'appointments/<str:token>/<int:appointment>/cancel/',
        CancelAppointmentView.as_view(),
        name='cancel_appointment'
    ),
]
