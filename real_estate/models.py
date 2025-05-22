from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from .validators import validate_image_size

# Create your models here.
class Client(models.Model):
    ROLE_BUYER = 'B'
    ROLE_SELLER = 'S'
    ROLE_ADMIN = 'A'
    ROLE_CHOICES = [
        (ROLE_BUYER, 'Buyer'),
        (ROLE_SELLER, 'Seller'),
        (ROLE_ADMIN, 'Admin'),
    ]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_BUYER)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"
    
    class Meta:
        ordering = ['user__first_name', 'user__last_name']
    
class Property(models.Model):
    PROPERTY_TYPE_HOUSE = 'house'
    PROPERTY_TYPE_APARTMENT = 'apartment'
    PROPERTY_TYPE_LAND = 'land'
    PROPERTY_TYPE_CHOICES = [
        (PROPERTY_TYPE_HOUSE, 'House'),
        (PROPERTY_TYPE_APARTMENT, 'Apartment'),
        (PROPERTY_TYPE_LAND, 'Land'),
    ]

    STATUS_FOR_SELL = 'for sale'
    STATUS_SOLD = 'sold'
    STATUS_PENDING = 'pending'
    STATUS_CHIOCES = [
        (STATUS_FOR_SELL, 'For Sale'),
        (STATUS_SOLD, 'Sold'),
        (STATUS_PENDING, 'Pending'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=10)
    zipcode = models.IntegerField()
    bedroom = models.IntegerField()
    bathroom = models.IntegerField()
    square_feet = models.IntegerField()
    lot_size = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPE_CHOICES, default=PROPERTY_TYPE_HOUSE)
    status = models.CharField(max_length=20, choices=STATUS_CHIOCES, default=STATUS_FOR_SELL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='properties')

    def __str__(self):
        return f"{self.title} - ${self.price}"
    
    class Meta:
        ordering = ['created_at']

class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(validators=[validate_image_size], upload_to='real_estate/images', blank=True, null=True)
    caption = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Image for {self.property.title}"

class Feature(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class PropertyFeature(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='features')
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.feature.name} for {self.property.title}"

class Inquiry(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='inquiries')
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    responded = models.BooleanField(default=False)

    def __str__(self):
        return f"Inquiry on {self.property.title} by {self.buyer.username}"