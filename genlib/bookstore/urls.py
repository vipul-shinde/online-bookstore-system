from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sign-up.html', views.signup, name='signup'),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate'),
    path('signup-confirmation.html', views.signup_confirmation, name='signup-confirmation'),
    path('login.html', views.login, name='login'),
    path('productDetails/<str:title>/', views.book_detail, name='book-details')
]
