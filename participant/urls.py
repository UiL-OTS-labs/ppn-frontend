from django.urls import include, path

from participant.views import AuthenticatedRegisterView, CancelAppointmentView, \
    CancelLandingView, ClosedExperimentView, CreateAccountView, \
    MyAppointmentsView, RegisterView, SubscribeToMailinglistView, \
    UnsubscribeFromMailinglistView

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

    path('create_account/', CreateAccountView.as_view(), name='create_account'),

    path(
        'unsubscribe_mailinglist/<str:token>/',
        UnsubscribeFromMailinglistView.as_view(),
        name='unsubscribe_mailinglist'
    ),

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
