import os
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User


def upload_image_path(instance, filename):
    ext = filename.split('.')[-1]
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

    if isinstance(instance, Service):
        folder = f'services/{instance.name}'
        new_filename = f'{instance.name}_{timestamp}.{ext}'
    elif isinstance(instance, ServiceItem):
        folder = f'service_items/{instance.name}/main'
        new_filename = f'{instance.name}_main_{timestamp}.{ext}'
    elif isinstance(instance, ServiceItemImage):
        folder = f'service_items/{instance.service_item.name}/gallery'
        new_filename = f'{instance.service_item.name}_gallery_{timestamp}.{ext}'
    else:
        folder = 'uploads/others'
        new_filename = f'file_{timestamp}.{ext}'

    return os.path.join(folder, new_filename)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, unique=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.phone_number


class Service(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to=upload_image_path, blank=True, null=True)
    popular = models.BooleanField(default=False)
    shutdown = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ServiceItem(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    duration_minutes = models.PositiveIntegerField(blank=True, null=True)
    main_image = models.ImageField(upload_to=upload_image_path, blank=True, null=True)
    popular = models.BooleanField(default=False)
    shutdown = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('service', 'name')

    def __str__(self):
        return f"{self.name} ({self.service.name})"


class ServiceItemImage(models.Model):
    service_item = models.ForeignKey(ServiceItem, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ImageField(upload_to=upload_image_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.service_item.name}"


class CartItem(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='cart_items')
    service_item = models.ForeignKey(ServiceItem, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)


class FavoriteItem(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='favorite_items')
    service_item = models.ForeignKey(ServiceItem, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
    


class Order(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('confirmed', 'Confirmed'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled')
        ],
        default='pending'
    )
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Order #{self.id} by {self.user.phone_number}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    service_item = models.ForeignKey(ServiceItem, on_delete=models.CASCADE)
    price_at_order_time = models.DecimalField(max_digits=10, decimal_places=2)
    added_at = models.DateTimeField(auto_now_add=True)