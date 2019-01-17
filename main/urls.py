from django.contrib.auth import views as auth_views
from django.urls import path

from .views import HomeView, CustomLoginView


app_name = 'main'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', HomeView.as_view(), name='home'),

]
