from django.urls import path

from .views import ExperimentsView, ProfileView


app_name = 'leader'

urlpatterns = [
    path('', ExperimentsView.as_view(), name='experiments'),
    path('profile/', ProfileView.as_view(), name='profile'),
]
