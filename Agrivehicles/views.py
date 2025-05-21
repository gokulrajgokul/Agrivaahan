from django.http import Http404, HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Avg
import json
from .models import Vehicle, Order, Contact, UserProfile, Rating, Booking, VehicleReview
from django.contrib.admin.views.decorators import staff_member_required

def index(request):
    vehicles = Vehicle.objects.all()
    return render(request, 'index.html', {'carousel_images': vehicles})

def about(request):
    return render(request, 'about.html')

def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        number = request.POST.get('number')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('confirm_password')
        role = request.POST.get('role')

        if not all([username, number, email, password, password2, role]):
            messages.error(request, "All fields are required")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already taken")
            return redirect('register')

        if len(number) != 10:
            messages.error(request, "Invalid mobile number")
            return redirect('register')

        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters")
            return redirect('register')

        if password != password2:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        profile = UserProfile.objects.create(
            user=user,
            phone=number,
            email=email,
            role=role,
        )
        profile.save()

        messages.success(request, "Your account has been created successfully!")
        return redirect('signin')

    return render(request, 'register.html')

def signin(request):
    if request.method == "POST":
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        if not loginusername or not loginpassword:
            messages.error(request, "All fields are required")
            return redirect('signin')

        user = authenticate(username=loginusername, password=loginpassword)
        if user is not None:
            login(request, user)

            if user.is_superuser:
                return redirect('home')

            try:
                user_profile = UserProfile.objects.get(user=user)
                return redirect('home') if user_profile.role == 'owner' else redirect('vehicles')
            except UserProfile.DoesNotExist:
                messages.error(request, "User profile not found.")
                return redirect('signin')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('signin')

    return render(request, 'login.html')

def signout(request):
    logout(request)
    return redirect('signin')

@login_required
def add_vehicle(request):
    vehicle_to_edit = None
    vehicle_id = request.GET.get('update_id')  # Fetch from URL to edit

    if vehicle_id:
        vehicle_to_edit = get_object_or_404(Vehicle, pk=vehicle_id, owner=request.user)

    if request.method == 'POST':
        vehicle_id = request.POST.get('id')  # ID is now the correct field name in the form
        name = request.POST.get('Vehicle_name')
        desc = request.POST.get('Vehicle_desc')
        price = request.POST.get('price')
        image = request.FILES.get('image')  # Handling file uploads properly
        owner_location = request.POST.get('owner_location')
        is_available = request.POST.get('is_available') == 'on'  # Checkbox logic
        delivery_time_0_10 = request.POST.get('delivery_time_0_10')
        delivery_time_10_20 = request.POST.get('delivery_time_10_20')

        if vehicle_id:  # Edit existing vehicle
            vehicle = get_object_or_404(Vehicle, pk=vehicle_id, owner=request.user)
            vehicle.Vehicle_name = name
            vehicle.Vehicle_desc = desc
            vehicle.price = price
            vehicle.owner_location = owner_location
            vehicle.is_available = is_available
            vehicle.delivery_time_0_10 = delivery_time_0_10
            vehicle.delivery_time_10_20 = delivery_time_10_20
            if image:
                vehicle.image = image
            vehicle.save()
            messages.success(request, "Vehicle updated successfully!")
        else:  # Add new vehicle
            Vehicle.objects.create(
                Vehicle_name=name,
                Vehicle_desc=desc,
                price=price,
                image=image,
                owner=request.user,  # Ensure the logged-in user is the owner
                owner_location=owner_location,
                is_available=is_available,
                delivery_time_0_10=delivery_time_0_10,
                delivery_time_10_20=delivery_time_10_20,
            )
            messages.success(request, "Vehicle added successfully!")

        return redirect('add_vehicle')  # Redirect after saving

    vehicles = Vehicle.objects.filter(owner=request.user)  # Fetch vehicles for the current user
    return render(request, 'add_vehicle.html', {'vehicles': vehicles, 'vehicle_to_edit': vehicle_to_edit})

@login_required
def delete_vehicle(request, id):
    vehicle = get_object_or_404(Vehicle, id=id, owner=request.user)
    vehicle.delete()
    messages.success(request, "Vehicle deleted successfully!")
    return redirect('add_vehicle')

@login_required
def owner_bookings(request):
    bookings = Booking.objects.filter(vehicle__owner=request.user, visible_to_owner=True).order_by('created_at')
    return render(request, 'bookings.html', {'bookings': bookings})

@login_required
def delete_booking(request, id):
    booking = get_object_or_404(Booking, id=id)
    if booking.vehicle.owner != request.user:
        return HttpResponseForbidden("You are not allowed to delete this booking.")
    if request.method == "POST":
        booking.visible_to_owner = False
        booking.save()
        messages.success(request, "Booking deleted successfully.")
        return redirect('owner_bookings')

def vehicles(request):
    name_query = request.GET.get('name', '')
    location_query = request.GET.get('location', '')
    vehicles = Vehicle.objects.filter(is_available=True).annotate(avg_rating=Avg('ratings__stars'))

    if name_query:
        vehicles = vehicles.filter(Vehicle_name__icontains=name_query)
    if location_query:
        vehicles = vehicles.filter(owner_location__icontains=location_query)

    all_locations = Vehicle.objects.values_list('owner_location', flat=True).distinct()

    return render(request, 'vehicles.html', {
        'vehicles': vehicles,
        'name_query': name_query,
        'location_query': location_query,
        'all_locations': all_locations,
    })

@login_required
def farmer_bookings(request):
    bookings = Booking.objects.filter(farmer=request.user, visible_to_farmer=True).order_by('created_at')
    return render(request, 'farmer_bookings.html', {'bookings': bookings})

def delete_farmer_booking(request, id):
    booking = get_object_or_404(Booking, id=id,  farmer=request.user)
    if request.method == 'POST':
        booking.delete()
        messages.success(request, 'Booking deleted successfully.')
    return redirect('farmer_bookings')  

@login_required
def bill(request, id):
    vehicle = get_object_or_404(Vehicle, id=id)
    return render(request, 'bill.html', {'vehicle': vehicle})

@login_required
def order(request):
    if request.method == "POST":
        billname = request.POST.get('billname', '')
        billemail = request.POST.get('billemail', '')
        billphone = request.POST.get('billphone', '')
        billaddress = request.POST.get('billaddress', '')
        billcity = request.POST.get('billcity', '')
        vehicle_id = request.POST.get('vehicle_id')
        dayss = request.POST.get('dayss', '1')
        date = request.POST.get('date', '')
        location = request.POST.get('location', '')

        vehicle = get_object_or_404(Vehicle, id=vehicle_id)

        if not all([billname, billemail, billphone, billaddress, billcity, dayss, date, location]):
            messages.error(request, "All fields are required")
            return render(request, 'bill.html', {'vehicle': vehicle})

        try:
            duration = int(dayss)
        except ValueError:
            messages.error(request, "Invalid number of days.")
            return render(request, 'bill.html', {'vehicle': vehicle})

        total_amount = vehicle.price * duration

        booking = Booking.objects.create(
            vehicle=vehicle,
            farmer=request.user,
            booking_date=date,
            duration=duration,
            total_amount=total_amount
        )
        vehicle.is_available = False
        vehicle.save()

        send_mail(
            'New Booking Notification',
            f"Vehicle '{vehicle.Vehicle_name}' booked by {billname}.\nPhone: {billphone}\nLocation: {location}\nDuration: {duration} days\nDate: {date}\nTotal: ₹{total_amount}",
            settings.EMAIL_HOST_USER,
            [vehicle.owner.email],
        )

        return render(request, 'confirmbooking.html', {'booking': booking})

    return redirect('home')

def contact(request):
    if request.method == "POST":
        contactname = request.POST.get('contactname', '')
        contactemail = request.POST.get('contactemail', '')
        contactnumber = request.POST.get('contactnumber', '')
        contactmsg = request.POST.get('contactmsg', '')

        if not all([contactname, contactemail, contactnumber, contactmsg]):
            messages.error(request, "All fields are required")
            return redirect('contact')

        if len(contactnumber) != 10:
            messages.error(request, "Invalid mobile number")
            return redirect('contact')

        Contact.objects.create(name=contactname, email=contactemail, phone_number=contactnumber, message=contactmsg)
        messages.success(request, "Your message has been sent.")

         
    return render(request, 'contact.html')
 
 
@csrf_exempt
@login_required
def submit_rating(request):
    if request.method == "POST":
        try:
            vehicle_id = request.POST.get('id')
            stars = int(request.POST.get('stars'))

            if not (1 <= stars <= 5):
                return JsonResponse({'success': False, 'error': 'Stars must be between 1 and 5'})

            vehicle = Vehicle.objects.get(id=vehicle_id)

      

            rating, created = Rating.objects.update_or_create(
                user=request.user,
                vehicle=vehicle,
                defaults={'stars': stars}
            )

            # Recalculate average
            avg_rating = Rating.objects.filter(vehicle=vehicle).aggregate(avg=Avg('stars'))['avg']
           
            # return JsonResponse({'success': True, 'new_avg': round(avg_rating, 1)})
            return JsonResponse({'success': True, 'new_avg': avg_rating})

        except Vehicle.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Vehicle not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})



def confirmbooking(request):
    return render(request, 'confirmbooking.html')

def custom_404(request, exception):
    return render(request, '404.html', status=404)

@login_required
@csrf_exempt
def update_profile(request):
    if request.method == 'POST':
        user = request.user
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        role = request.POST.get('role')

        user.username = username
        user.email = email
        user.save()

        user_profile, _ = UserProfile.objects.get_or_create(user=user)
        user_profile.phone = phone
        user_profile.role = role
        user_profile.save()

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

def get_user_role(request):
    username = request.GET.get('username')
    if username:
        try:
            user = User.objects.get(username=username)
            user_profile = UserProfile.objects.get(user=user)
            return JsonResponse({'role': user_profile.role})
        except:
            return JsonResponse({'role': 'unknown'})
    return JsonResponse({'role': 'unknown'})

@csrf_exempt
@login_required
def submit_review(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        rating = data.get('rating')
        review = data.get('review')
        vehicle_id = data.get('id')

        vehicle = get_object_or_404(Vehicle, id=vehicle_id)

        VehicleReview.objects.create(
            vehicle=vehicle,
            user=request.user,
            rating=rating,
            review=review
        )
        return JsonResponse({'message': 'Review submitted successfully'})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def get_reviews(request, id):
    reviews = VehicleReview.objects.filter(vehicle__id=id).values('rating', 'review', 'user__username', 'created_at')
    # return JsonResponse(list(reviews), safe=False)
    return JsonResponse({'reviews': list(reviews)})



@staff_member_required
def all_messages(request):
    messages = Contact.objects.all().order_by('-created_at')
    return render(request, 'all_messages.html', {'messages': messages})