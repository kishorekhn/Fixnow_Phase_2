from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages  
from .models import UserProfile, ServiceItem, CartItem, Service,FavoriteItem
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from django.conf import settings
import smtplib
from email.message import EmailMessage

def login_view(request):
    if request.method == 'POST':
        phone = request.POST.get('phone_number')
        otp = '123456' 

        request.session['otp'] = otp
        request.session['phone_number'] = str(phone)
        
        # Dummy Otp Verification without twilio
        
        return redirect('verify_otp')

    return render(request, 'Auth/login.htm')

def logout_view(request):
    logout(request)
    return redirect('home')

def verify_otp_view(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        session_otp = request.session.get('otp')
        phone = request.session.get('phone_number')

        if entered_otp == session_otp:
            user_qs = User.objects.filter(username=phone)
            if user_qs.exists():
                user = user_qs.first()
                login(request, user)
                messages.info(request, "You are already registered and logged in.")
                return redirect('home')

            user = User.objects.create_user(username=phone)
            user_profile = UserProfile.objects.create(user=user, phone_number=phone, is_verified=True)

            login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect('home')
        else:
            return render(request, 'Auth/otp.htm', {'error': 'Invalid OTP'})

    return render(request, 'Auth/otp.htm')


def home(request):
    services = Service.objects.all() 
    return render(request, "Main/home.htm", {"services": services})

def services(request):
    services = Service.objects.prefetch_related('items').all()
    return render(request, 'Main/items.htm', {'services': services})


def service_items(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    items = ServiceItem.objects.filter(service_id=service_id)
    return render(request, "Main/services.htm", {"service": service, "items": items})


@login_required
def orders_view(request):
    user_profile = UserProfile.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(user=user_profile).select_related('service_item')

    return render(request, 'Main/cart.htm', {'cart_items': cart_items})

@login_required
def favorites_view(request):
    user_profile = UserProfile.objects.get(user=request.user)
    favorite_items = FavoriteItem.objects.filter(user=user_profile).select_related('service_item')

    return render(request, 'Main/favorites.htm', {'favorite_items': favorite_items})


@csrf_exempt
@login_required
def toggle_cart(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        item_id = data.get('item_id')

        try:
            service_item = ServiceItem.objects.get(id=item_id)

            user_profile, created = UserProfile.objects.get_or_create(
                user=request.user,
                defaults={
                    'phone_number': f'999{request.user.id}',
                    'is_verified': True
                }
            )

            cart_item, created = CartItem.objects.get_or_create(
                user=user_profile,
                service_item=service_item
            )

            if not created:
                cart_item.delete()
                return JsonResponse({'status': 'removed'})
            else:
                return JsonResponse({'status': 'added'})

        except ServiceItem.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Item not found'}, status=404)

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)



@csrf_exempt
@login_required
def toggle_favorite(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        item_id = data.get('item_id')

        try:
            service_item = ServiceItem.objects.get(id=item_id)

            user_profile, created = UserProfile.objects.get_or_create(
                user=request.user,
                defaults={
                    'phone_number': f'999{request.user.id}',
                    'is_verified': True
                }
            )

            favorite_item, created = FavoriteItem.objects.get_or_create(
                user=user_profile,
                service_item=service_item
            )

            if not created:
                favorite_item.delete()
                return JsonResponse({'status': 'removed'})
            else:
                return JsonResponse({'status': 'added'})

        except ServiceItem.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Item not found'}, status=404)

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

def contact_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        service = request.POST.get('service')
        message = request.POST.get('message')
        urgent = 'Yes' if request.POST.get('urgentService') == 'on' else 'No'

        subject = f"New Contact Form Submission - {service.title()}"
        body = f"""
You have received a new message from your website contact form.

Name: {first_name} {last_name}
Email: {email}
Phone: {phone}
Service Needed: {service}
Urgent Request: {urgent}

Message:
{message}
"""

        try:
            msg = EmailMessage()
            msg['Subject'] = subject
            msg['From'] = settings.EMAIL_HOST_USER
            msg['To'] = settings.EMAIL_HOST_USER
            msg.set_content(body)

            with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                smtp.starttls()
                smtp.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
                smtp.send_message(msg)

            return render(request, 'Main/contact.htm', {'success': True})

        except Exception as e:
            print(f"Email sending failed: {e}")
            return render(request, 'Main/contact.htm', {'error': True})

    return render(request, 'Main/contact.htm')