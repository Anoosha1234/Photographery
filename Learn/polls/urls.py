from django.urls import path

from . import views


urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    path('categories/', views.CategoryView.as_view(), name='categories'),
    path('BookingCategories/<int:pk>', views.CategoryDetailView.as_view(), name='category-detail')
]
