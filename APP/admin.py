from django.contrib import admin

# Register your models here.

from .models import UserProfile, Service, ServiceItem, ServiceItemImage,CartItem,FavoriteItem,Order,OrderItem

admin.site.register([UserProfile, Service, ServiceItem, ServiceItemImage,CartItem,FavoriteItem,Order,OrderItem])