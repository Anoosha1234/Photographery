from django.db import models

class User(models.Model):
    user_first_name = models.CharField(max_length=50)
    user_last_name = models.CharField(max_length=50)
    user_email = models.EmailField(max_length=30)
    user_password = models.CharField(max_length=50)
    user_account_name = models.CharField(max_length=30)
    is_super_user = models.BooleanField()

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

class BookingCategories(models.Model):
    category_type  = models.CharField(max_length=40)
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

class ServiceDetails(models.Model):
    service_name = models.ForeignKey(BookingCategories, on_delete=models.CASCADE)
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    begins_at = models.DateTimeField()
    ends_at = models.DateTimeField()

    def __str__(self):
        return str(self.service_name)

    class Meta:
        db_table="ServiceDetails"
        verbose_name_plural = 'Service Details'


class CurrentBookings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(ServiceDetails, on_delete=models.CASCADE)
    fulfillment = models.BooleanField()
    has_paid = models.BooleanField()

    def __str__(self):
        return str(self.service)

    class Meta:
        verbose_name_plural = 'Current Bookings'


class UserHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_service = models.ForeignKey(CurrentBookings, on_delete=models.CASCADE)
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
    photographer_expertise = models.CharField(max_length=40)
    photographer_experience = models.IntegerField()
    photographer_pay = models.IntegerField()

    class Meta:
        ordering = ['photographer_last_name', 'photographer_first_name']
        verbose_name_plural = 'Photographers'

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.photographer_last_name}, {self.photographer_first_name}'
