from django.contrib import admin

admin.site.site_header = "Photographery Admin"
admin.site.index_title = "Welcome to Photographery"
admin.site.site_title = "Photographery"

from .models import User
from .models import UserAddress
from .models import UserHistory
from .models import BookingCategories
from .models import Photographers
from .models import BookApointment
from .models import WebsiteForm
#admin.site.register(User)
#admin.site.register(UserAddress)
#admin.site.register(UserReviews)
#admin.site.register(BookingCategories)
#admin.site.register(Photographers)
#admin.site.register(ServiceDetails)


class UserAddressInline(admin.TabularInline):
    model = UserAddress

# Define the admin class
class UserAdmin(admin.ModelAdmin):
    list_display = ('id','user_first_name', 'user_last_name', 'user_account_name')
    inlines = [UserAddressInline]

admin.site.register(User, UserAdmin)


# Register the Admin classes for UserAddress using the decorator
@admin.register(UserAddress)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_city', 'user_country', 'user_zip_code')

# Register the Admin classes for BookingCategories using the decorator
@admin.register(BookingCategories)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'category_type', 'category_duration', 'category_price')


# Register the Admin classes for Photographers using the decorator
@admin.register(Photographers)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('photographer_first_name', 'photographer_last_name', 'photographer_expertise', 'photographer_experience')

# Register the Admin classes for UserHistory using the decorator
@admin.register(UserHistory)
class UserHistory(admin.ModelAdmin):
    list_display = ('user', 'user_service')
    list_filter = ('user', 'user_service')

@admin.register(BookApointment)
class BookApointment(admin.ModelAdmin):
    list_display = ('user_booking_name', 'user_booking_phone', 'user_booking_datetime', 'user_booking_category','user_booking_photographer','user_booking_address')

@admin.register(WebsiteForm)
class WebsiteForm(admin.ModelAdmin):
    list_display = ('your_name', 'your_email', 'subject','message')
