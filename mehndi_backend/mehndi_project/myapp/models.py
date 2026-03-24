from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class USERS(models.Model):
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=200)
    pincode = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    LOGIN = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10)
    latitude = models.CharField(max_length=100)
    longitude = models.CharField(max_length=100)
    
    
class Artist(models.Model):
    LOGIN = models.OneToOneField(User, on_delete=models.CASCADE)
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=150)
    email = models.CharField(max_length=150)
    phone = models.CharField(max_length=15)
    profile_image = models.ImageField(upload_to='artist_profiles/', blank=True, null=True)
    experience_years = models.IntegerField(default=0)
    specialization = models.CharField(max_length=200, help_text="Bridal, Arabic, Traditional etc.")
    bio = models.TextField(blank=True)
    address = models.TextField()
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    status=models.CharField(max_length=100)

class MehndiDesign(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, limit_choices_to={'role': 'artist'})
    image = models.ImageField(upload_to='mehndi_designs/')
    design_type = models.CharField(max_length=20)
    hand_size = models.CharField(max_length=10)
    coverage = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_approved = models.BooleanField(default=False)
    date=models.CharField(max_length=100)

class Booking(models.Model):
    user = models.ForeignKey(USERS, on_delete=models.CASCADE)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    booking_date = models.DateField()
    booking_time = models.TimeField()
    status = models.CharField(max_length=20, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    amount = models.CharField(max_length=100, default='0.00')

class Feedback(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class complaint(models.Model):
    user = models.ForeignKey(USERS, on_delete=models.CASCADE)
    complaint_text = models.TextField()
    reply_text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class HennaProduct(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2, default=40.00)
    stock = models.IntegerField()
    image = models.ImageField(upload_to='henna_products/')
    is_approved = models.CharField(max_length=100, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

class Order(models.Model):
    user = models.ForeignKey(USERS, on_delete=models.CASCADE)
    product = models.ForeignKey(HennaProduct, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending')


class Chat(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    message = models.TextField()
    timestamp = models.CharField(max_length=100)
    image=models.CharField(max_length=1000)
    message_type=models.CharField(max_length=100)




class Mehndi(models.Model):

    STYLE_CHOICES = (
        ('Arabic', 'Arabic'),
        ('Bridal', 'Bridal'),
        ('Floral', 'Floral'),
    )

    name = models.CharField(max_length=100)
    style = models.CharField(max_length=50, choices=STYLE_CHOICES)

    palm_width_ratio = models.FloatField()
    finger_length_ratio = models.FloatField()

    design_image = models.ImageField(upload_to='mehndi_designs/')

