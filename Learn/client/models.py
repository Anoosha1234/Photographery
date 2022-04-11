from django.db import models
from django_enumfield import enum
from django.utils.translation import ugettext_lazy

class User(models.Model):
    user_first_name = models.CharField(max_length=30)
    user_last_name = models.CharField(max_length=30)
    user_email = models.EmailField(max_length=30)
    user_password = models.CharField(max_length=30)
    user_account_name = models.CharField(max_length=60)

    def __str__(self):
        return self.user_first_name

    class Meta:
        ordering = ['-user_first_name']
        verbose_name_plural = 'User'

class UserAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_city = models.CharField(max_length=30)
    user_district = models.CharField(max_length=30)
    user_country = models.CharField(max_length=50)
    user_zip_code = models.IntegerField()
    user_street = models.CharField(max_length=30)
    user_house_number = models.IntegerField()

    def __str__(self):
        return str(self.user.user_first_name)

    class Meta:
        verbose_name_plural = 'User Address'


class Category_types(enum.Enum):
    Wedding = 0
    Portraits = 1
    Fashion = 2
    Formal_Events = 3
    Tourism = 4
    Portfolio = 5

    __labels__ = {
        Formal_Events: ugettext_lazy("Formal Events")
    }


class BookingCategories(models.Model):
    category_type  = enum.EnumField(Category_types, default=Category_types.Wedding)
    category_name = models.CharField(max_length=40)
    category_duration = models.DurationField()
    category_price = models.DecimalField(max_digits = 5, decimal_places = 2)

    def __str__(self):
        return self.category_name

    def get_absolute_url(self):
        """Returns the url to access a particular instance of the model."""
        return reverse('category-detail-view', args=[str(self.id)])

    class Meta:
        verbose_name_plural = 'Booking Categories'


class UserHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_service = models.ForeignKey(BookingCategories, on_delete=models.CASCADE)
    fulfillment = models.BooleanField()
    order_date = models.DateField()

    class Meta:
        db_table = 'UserHistory'
        verbose_name_plural = 'User History'

    def __str__(self):
        return str(self.user)


class Photographers(models.Model):
    photographer_first_name = models.CharField(max_length=40)
    photographer_last_name = models.CharField(max_length=40)
    photographer_expertise = enum.EnumField(Category_types, default=Category_types.Wedding)
    photographer_experience = models.IntegerField()
    photographer_pay = models.DecimalField(max_digits = 5, decimal_places = 2)

    class Meta:
        ordering = ['photographer_last_name', 'photographer_first_name']
        verbose_name_plural = 'Photographers'

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.photographer_last_name}, {self.photographer_first_name}'

class BookApointment(models.Model):
    user_booking_name = models.CharField(max_length=30)
    user_booking_phone = models.CharField(max_length=30)
    user_booking_datetime = models.DateTimeField()
    user_booking_category = models.ForeignKey(BookingCategories, on_delete=models.CASCADE)
    user_booking_photographer = models.ForeignKey(Photographers, on_delete=models.CASCADE)
    user_booking_address = models.CharField(max_length=30)

    def __str__(self):
        return str(f'{self.user_booking_name}, {self.user_booking_phone}, {self.user_booking_datetime}, {self.user_booking_category}, {self.user_booking_photographer}, {self.user_booking_address}')

    class Meta:
        verbose_name_plural = 'Book Appointment'

class WebsiteForm(models.Model):
    your_name = models.CharField(max_length=50)
    your_email = models.EmailField(max_length=30)
    subject = models.CharField(max_length=200)
    message = models.CharField(max_length=700)

    def _str_(self):
        return str(self.your_name)

    class Meta:
        verbose_name_plural = 'Website Form'
