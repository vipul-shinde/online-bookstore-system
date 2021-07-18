from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup, name='signup'),
    path('signup_confirmation', views.signup_confirmation, name='signup_confirmation'),
]