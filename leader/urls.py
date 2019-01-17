from django.urls import path

from .views import ExperimentsView


app_name = 'leader'

urlpatterns = [
    path('', ExperimentsView.as_view(), name='experiments'),

]
