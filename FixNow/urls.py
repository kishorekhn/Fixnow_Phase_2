
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from APP import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('services/', views.services, name='services'),
    path('services/<int:service_id>/', views.service_items, name='service_items'),
    path('verify-otp/', views.verify_otp_view, name='verify_otp'),
    path('toggle-cart/', views.toggle_cart, name='toggle_cart'), 
    path('toggle-favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('orders/', views.orders_view, name='orders'),
    path('favorites/', views.favorites_view, name='favorites'),
    path('contact',views.contact_view, name='contact'),

    path('adminn/', views.staff_login, name='staff_login'),
    path('adminn/addcategory/', views.add_category, name='add_category'),
    path('adminn/deletecategory/<int:pk>/', views.delete_category, name='delete_category'),
    path('adminn/updatecategory/<int:pk>/', views.update_category, name='update_category'),
    path('adminn/addservices/', views.add_service_item, name='add_service_item'),
    path('adminn/deleteserviceitem/<int:pk>/', views.delete_service_item, name='delete_service_item'),
    path('adminn/updateserviceitem/<int:pk>/', views.update_service_item, name='update_service_item'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)