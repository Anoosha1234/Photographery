from django.urls import path

from . import views


urlpatterns = [
    # ex: /polls/
    path('', views.home, name='home'),
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('order', views.order, name='order'),
    
    # path('categories/', views.CategoryView.as_view(), name='categories'),
    # path('BookingCategories/<int:pk>', views.CategoryDetailView.as_view(), name='category-detail')
]