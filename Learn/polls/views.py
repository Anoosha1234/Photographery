from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic
from .models import User, UserAddress, BookingCategories, ServiceDetails, CurrentBookings, UserHistory, Photographers

def index(request):

    # Generate counts of some of the main objects
    num_users = User.objects.all().count()
    booking_categories = BookingCategories.objects.all().count()
    num_bookings = CurrentBookings.objects.count()

    context = {
        'num_users': num_users,
        'booking_categories': booking_categories,
        'num_bookings': num_bookings,
    }


    return render(request, 'polls/index.html', context=context)

class CategoryView(generic.ListView):
    model = BookingCategories

class CategoryDetailView(generic.DetailView):
    model = BookingCategories
