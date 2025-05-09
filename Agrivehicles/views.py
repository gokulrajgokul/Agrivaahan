from django.http import Http404, HttpResponse, HttpResponseForbidden
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import Vehicle, Order, Contact ,UserProfile,Rating,Booking, VehicleReview
from django.http import JsonResponse 
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json
from django.db.models import Avg

# Create your views here.

def index(request):
    vehicles = Vehicle.objects.all()
    return render(request,'index.html',{'carousel_images': vehicles})
def about(request):
    return render(request,'about.html ')
 

def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        number = request.POST.get('number')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        role = request.POST.get('role')  # 🔹 Get selected role from form

        # Validation
        if not username or not email or not password or not password2 or not number or not role:
            messages.error(request, "All fields are required")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already taken")
            return redirect('register')
        
        if len(number) != 10:
            messages.error(request, "Invalid mobile Number")
            return redirect('register')
        if len(password) < 8:
            messages.error(request, "password must contain atleast 8 characters")
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

            # Superuser login bypasses profile role check
            if user.is_superuser:
                return redirect('home')  # Django admin page
            try:
                user_profile = UserProfile.objects.get(user=user)
                if user_profile.role == 'owner':
                    return redirect('home')
                else:
                    return redirect('vehicles')
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

   
    update_id = request.GET.get('update_id')
    if update_id:
        vehicle_to_edit = get_object_or_404(Vehicle, pk=update_id, owner=request.user)

    if request.method == 'POST':
        name = request.POST.get('Vehicle_name')
        desc = request.POST.get('Vehicle_desc')
        price = request.POST.get('price')
        image = request.FILES.get('image')
        owner_location = request.POST.get('owner_location')
        is_available = request.POST.get('is_available') == 'on'  # <- New line
        vehicle_id = request.POST.get('vehicle_id')
        delivery_time_0_10 = request.POST.get('delivery_time_0_10')
        delivery_time_10_20 = request.POST.get('delivery_time_10_20')

        if vehicle_id:
           
            vehicle = get_object_or_404(Vehicle, pk=vehicle_id, owner=request.user)
            vehicle.Vehicle_name = name
            vehicle.Vehicle_desc = desc
            vehicle.price = price
            vehicle.owner_location = owner_location
            vehicle.is_available = is_available   
            vehicle.delivery_time_0_10 = delivery_time_0_10,
            vehicle.delivery_time_10_20 = delivery_time_10_20,
            if image:
                vehicle.image = image
            vehicle.save()
            messages.success(request, "Vehicle updated successfully!")
        else:
            
            Vehicle.objects.create(
                Vehicle_name=name,
                Vehicle_desc=desc,
                price=price,
                image=image,
                owner=request.user,
                owner_location=owner_location,
                is_available=is_available,   
                delivery_time_0_10=delivery_time_0_10 ,
                delivery_time_10_20=delivery_time_10_20 ,
            )
            messages.success(request, "Vehicle added successfully!")

        return redirect('add_vehicle')

    vehicles = Vehicle.objects.filter(owner=request.user)
    return render(request, 'add_vehicle.html', {
        'vehicles': vehicles,
        'vehicle_to_edit': vehicle_to_edit
    })



@login_required
def delete_vehicle(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk, owner=request.user)
    vehicle.delete()
    messages.success(request, "Vehicle deleted successfully!")
    return redirect('add_vehicle')  

@login_required
def owner_bookings(request):
    owner = request.user
    bookings = Booking.objects.filter(vehicle__owner=owner, visible_to_owner=True).order_by('created_at')
    return render(request, 'bookings.html', {'bookings': bookings})

@login_required
def delete_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Ensure only the vehicle owner can delete this booking
    if booking.vehicle.owner != request.user:
        return HttpResponseForbidden("You are not allowed to delete this booking.")
    
    if request.method == "POST":
        booking.visible_to_owner = False  # Hide from owner's view
        booking.save()
        # booking.delete()
        messages.success(request, "Booking deleted successfully.")
        return redirect('owner_bookings')
 












 






def vehicles(request):
    name_query = request.GET.get('name', '')
    location_query = request.GET.get('location', '')

    vehicles = Vehicle.objects.all().annotate(avg_rating=Avg('ratings__stars'))

    if name_query:
        vehicles = vehicles.filter(Vehicle_name__icontains=name_query)

    if location_query:
        vehicles = vehicles.filter(owner_location__icontains=location_query)

    # Get distinct locations for dropdown
    all_locations = Vehicle.objects.values_list('owner_location', flat=True).distinct()

    return render(request, 'vehicles.html', {
        'vehicles': vehicles,
        'name_query': name_query,
        'location_query': location_query,
        'all_locations': all_locations,
    })






@login_required
def farmer_bookings(request):
    farmer = request.user
    bookings = Booking.objects.filter(farmer=farmer, visible_to_farmer=True).order_by('created_at')
    return render(request, 'farmer_bookings.html', {'bookings': bookings})

@login_required
def delete_farmer_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, farmer=request.user)
    booking.visible_to_farmer = False  # Soft-delete for farmer
    booking.save()
    # booking.delete()
    messages.success(request, "Booking deleted successfully.")
    return redirect('farmer_bookings')


# def bill(request):
#     Vehicles= Vehicle.objects.all()
#     params = {'vehicles':Vehicles}
#     return render(request,'bill.html',params)
 
def bill(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    return render(request, 'bill.html', {'vehicle': vehicle})



 


 


  
 

@login_required
def order(request):
    if request.method == "POST":
        # Get form data
        billname = request.POST.get('billname', '')
        billemail = request.POST.get('billemail', '')
        billphone = request.POST.get('billphone', '')
        billaddress = request.POST.get('billaddress', '')
        billcity = request.POST.get('billcity', '')
        vehicle_id = request.POST.get('vehicle_id')
        dayss = request.POST.get('dayss', '1')
        date = request.POST.get('date', '')
        location = request.POST.get('location', '')

        # Get the vehicle (needed for bill.html)
        vehicle = get_object_or_404(Vehicle, id=vehicle_id)

        # Check for empty fields
        if not billname or not billemail or not billphone or not billaddress or not billcity or not dayss or not date or not location:
            messages.error(request, "All fields are required")
            return render(request, 'bill.html', {
                'vehicle': vehicle,
            })  # stays on same page

        # Check if days is valid number
        try:
            duration = int(dayss)
        except ValueError:
            messages.error(request, "Invalid number of days.")
            return render(request, 'bill.html', {
                'vehicle': vehicle,
            })

        total_amount = vehicle.price * duration

        # Save booking
        booking = Booking.objects.create(
            vehicle=vehicle,
            farmer=request.user,
            booking_date=date,
            duration=duration,
            total_amount=total_amount
        )

        # Send email to vehicle owner
        send_mail(
            'New Booking Notification',
            f"A new booking has been made for your vehicle '{vehicle.Vehicle_name}' by {billname}.\n\n"
            f"Details:\n"
            f"Name: {billname}\n"
            
            f"Phone: {billphone}\n"
            f"Location: {location}\n"
            f"Duration: {duration} days\n"
            f"Total Amount: {total_amount}\n\n"
            f"Booking Date: {date}\n\n"
            f"Please log in to your account to view more details.",
            settings.EMAIL_HOST_USER,  # Sender's email (from settings)
            [vehicle.owner.email],  # Owner's email (associated with the vehicle)
        )

        return render(request, 'confirmbooking.html', {'booking': booking})

    return redirect('home')



def contact(request):
    if request.method == "POST":
        contactname = request.POST.get('contactname','')
        contactemail = request.POST.get('contactemail','')
        contactnumber = request.POST.get('contactnumber','')
        contactmsg = request.POST.get('contactmsg','')

        if not contactname or not contactnumber or not contactemail or not contactmsg  :
            messages.error(request, "All fields are required")
            return redirect('contact')


        if len(contactnumber) != 10:
            messages.error(request, "Invalid mobile Number")
            return redirect('contact')

        contact = Contact(name = contactname, email = contactemail, phone_number = contactnumber,message = contactmsg)
        contact.save()
    return render(request,'contact.html ')
 



 
@csrf_exempt
@login_required
def submit_rating(request):
    if request.method == "POST":
        try:
            vehicle_id = request.POST.get('vehicle_id')
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
@csrf_exempt  # Disable CSRF for simplicity (not recommended for production)
def update_profile(request):
    if request.method == 'POST':
        user = request.user
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        role = request.POST.get('role')

        # Update user details
        user.username = username
        user.email = email
        user.save()

        # Update profile details (if user profile exists)
        if hasattr(user, 'userprofile'):
            user_profile = user.userprofile
        else:
            user_profile = UserProfile(user=user)

        user_profile.phone = phone
        user_profile.role = role
        user_profile.save()

        # Respond with success
        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
 

def get_user_role(request):
    username = request.GET.get('username')
    if username:
        try:
            user = User.objects.get(username=username)
            user_profile = UserProfile.objects.get(user=user)
            return JsonResponse({'role': user_profile.role})
        except User.DoesNotExist:
            return JsonResponse({'role': 'unknown'})
        except UserProfile.DoesNotExist:
            return JsonResponse({'role': 'unknown'})
    return JsonResponse({'role': 'unknown'})


@csrf_exempt
def submit_review(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        rating = data.get('rating')
        review = data.get('review')
        vehicle_id = data.get('vehicle_id')
        vehicle = Vehicle.objects.get(id=vehicle_id)

        VehicleReview.objects.create(
            vehicle=vehicle,
            user=request.user,
            rating=rating,
            review=review
        )
        return JsonResponse({'message': 'Review submitted successfully'})
    return JsonResponse({'error': 'Invalid request'}, status=400)
def get_reviews(request, vehicle_id):
    # Fetch reviews for the given vehicle ID
    reviews = VehicleReview.objects.filter(vehicle_id=vehicle_id).values('rating', 'review', 'user__username', 'created_at')
    
    # Convert queryset to a list of dictionaries
    reviews_data = list(reviews)
    
    # Return the reviews as JSON
    return JsonResponse({'reviews': reviews_data})