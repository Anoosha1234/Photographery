from django.urls import path
from django.contrib import admin
from . import views


urlpatterns = [
    # ex: /polls/
    path('', views.home, name='home'),
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('order', views.order, name='order'),
    path("logout", views.logout, name= "logout"),
    path('order_details',views.order_details, name='order_details'),
    path('user_details',views.user_details, name='user_details'),
    path('admin:index/', admin.site.urls, name='admin'),
    path('forgot_Password/', views.forgot_Password, name='forgot_Password'),
    path('forgotEmail/', views.forgotEmail, name='forgotEmail'),

]
