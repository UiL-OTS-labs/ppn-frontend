from django.urls import path

from participant.views import RegisterView

app_name = 'participant'

urlpatterns = [
    path('register/<int:experiment>/', RegisterView.as_view(), name='register'),

]
