from django.http import Http404, HttpResponse, HttpResponseForbidden
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import Vehicle, Order, Contact ,UserProfile,Rating,Booking
from django.http import JsonResponse 
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def index(request):
    vehicles = Vehicle.objects.all()
    return render(request,'index.html',{'carousel_images': vehicles})
def about(request):
    return render(request,'about.html ')

# def register(request):
#     if request.method == "POST":
#         username = request.POST.get('username')
#         number = request.POST.get('number')
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         password2 = request.POST.get('password2')

#         # Validation
#         if not username or not email or not password or not password2 or not number:
#             messages.error(request, "All fields are required")
#             return redirect('register')

#         if User.objects.filter(username=username).exists():
#             messages.error(request, "Username already taken")
#             return redirect('register')

#         if User.objects.filter(email=email).exists():
#             messages.error(request, "Email already taken")
#             return redirect('register')

#         if password != password2:
#             messages.error(request, "Passwords do not match")
#             return redirect('register')

#         # Create User in auth_user table
#         user = User.objects.create_user(username=username, email=email, password=password)
#         user.save()

#         # Store all details in UserProfile table
#         profile = UserProfile.objects.create(
#             user=user,
#             phone=number,
#             email=email,
            
#         )
#         profile.save()

#         messages.success(request, "Your account has been created successfully!")
#         return redirect('signin')  # Redirect to login page after registration

#     return render(request, 'register.html')



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

        # Create User in auth_user table
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        # Store all details in UserProfile table including role
        profile = UserProfile.objects.create(
            user=user,
            phone=number,
            email=email,
            role=role,  # 🔹 Save selected role
        )
        profile.save()

        messages.success(request, "Your account has been created successfully!")
        return redirect('signin')  # Redirect to login page after registration

    return render(request, 'register.html')

# def signin(request):
#     if request.method == "POST":
#         loginusername = request.POST['loginusername']
#         loginpassword = request.POST['loginpassword']

#         user = authenticate(username = loginusername,password = loginpassword)
#         if user is not None:
#             login(request, user)
#             # messages.success(request,"Successfully logged in!")
#             return redirect('vehicles')
#         else:
#             messages.error(request,"Invalid credentials")
#             return redirect('signin')

#     else:
#         print("error")
#         return render(request,'login.html')

  # make sure this import exists

# def signin(request):
#     if request.method == "POST":
#         loginusername = request.POST['loginusername']
#         loginpassword = request.POST['loginpassword']

#         if not loginusername or not loginpassword :
#             messages.error(request, "All fields are required")
#             return redirect('signin')

#         user = authenticate(username=loginusername, password=loginpassword)
#         if user is not None:
#             login(request, user)

#             try:
#                 user_profile = UserProfile.objects.get(user=user)
#                 if user_profile.role == 'owner':
#                     return redirect('home')  # Owner → Add Vehicle page
#                 else:
#                     return redirect('vehicles')  # Farmer → View Vehicles page
#             except UserProfile.DoesNotExist:
#                 messages.error(request, "User profile not found.")
#                 return redirect('signin')
#         else:
#             messages.error(request, "Invalid credentials")
#             return redirect('signin')

#     else:
#         return render(request, 'login.html')



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
        # messages.success(request,"Successfully logged out!")
        return redirect('signin')
    
    # return HttpResponse('signout')
 

# @login_required
# def add_vehicle(request):
#     if request.method == 'POST':
#         name = request.POST.get('Vehicle_name')
#         desc = request.POST.get('Vehicle_desc')
#         price = request.POST.get('price')
#         image = request.FILES.get('image')

#         Vehicle.objects.create(
#             Vehicle_name=name,
#             Vehicle_desc=desc,
#             price=price,
#             image=image,
#             owner=request.user 
#         )

#         messages.success(request, "Vehicle added successfully!")
#         return redirect('add_vehicle')  # or anywhere you want

#     return render(request, 'add_vehicle.html')


# from django.contrib import messages
# from django.shortcuts import render, redirect, get_object_or_404
# from .models import Vehicle
# from django.contrib.auth.decorators import login_required







# @login_required
# def add_vehicle(request):
#     vehicle_to_edit = None

#     # If updating
#     update_id = request.GET.get('update_id')
#     if update_id:
#         vehicle_to_edit = get_object_or_404(Vehicle, pk=update_id, owner=request.user)

#     if request.method == 'POST':
#         name = request.POST.get('Vehicle_name')
#         desc = request.POST.get('Vehicle_desc')
#         price = request.POST.get('price')
#         image = request.FILES.get('image')
#         owner_location = request.POST.get('owner_location')
#         vehicle_id = request.POST.get('vehicle_id')  # Hidden input for update

#         if vehicle_id:
#             # Update existing
#             vehicle = get_object_or_404(Vehicle, pk=vehicle_id, owner=request.user)
#             vehicle.Vehicle_name = name
#             vehicle.Vehicle_desc = desc
#             vehicle.price = price
#             vehicle.owner_location = owner_location
#             if image:
#                 vehicle.image = image
#             vehicle.save()
#             messages.success(request, "Vehicle updated successfully!")
#         else:
#             # Create new
#             Vehicle.objects.create(
#                 Vehicle_name=name,
#                 Vehicle_desc=desc,
#                 price=price,
#                 image=image,
#                 owner=request.user,
#                 owner_location=owner_location 
#             )
#             messages.success(request, "Vehicle added successfully!")

#         return redirect('add_vehicle')

#     vehicles = Vehicle.objects.filter(owner=request.user)
#     return render(request, 'add_vehicle.html', {
#         'vehicles': vehicles,
#         'vehicle_to_edit': vehicle_to_edit
#     })



@login_required
def add_vehicle(request):
    vehicle_to_edit = None

    # If updating
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

        if vehicle_id:
            # Update existing vehicle
            vehicle = get_object_or_404(Vehicle, pk=vehicle_id, owner=request.user)
            vehicle.Vehicle_name = name
            vehicle.Vehicle_desc = desc
            vehicle.price = price
            vehicle.owner_location = owner_location
            vehicle.is_available = is_available  # <- New line
            if image:
                vehicle.image = image
            vehicle.save()
            messages.success(request, "Vehicle updated successfully!")
        else:
            # Create new vehicle
            Vehicle.objects.create(
                Vehicle_name=name,
                Vehicle_desc=desc,
                price=price,
                image=image,
                owner=request.user,
                owner_location=owner_location,
                is_available=is_available  # <- New line
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

# def vehicles(request):
#     Vehicles = Vehicle.objects.all()
    
#     params = {'Vehicle':Vehicles}
#     return render(request,'vehicles.html',params)
def vehicles(request):
    name_query = request.GET.get('name', '')
    location_query = request.GET.get('location', '')

    vehicles = Vehicle.objects.all()  # ✅ Show all vehicles, regardless of availability

    if name_query:
        vehicles = vehicles.filter(Vehicle_name__icontains=name_query)

    if location_query:
        vehicles = vehicles.filter(owner_location__icontains=location_query)

    return render(request, 'vehicles.html', {
        'Vehicle': vehicles,
        'name_query': name_query,
        'location_query': location_query
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



 


 


 
# @login_required
# def order(request):
#     if request.method == "POST":
#         # Get form data
#         billname = request.POST.get('billname', '')
#         billemail = request.POST.get('billemail', '')
#         billphone = request.POST.get('billphone', '')
#         billaddress = request.POST.get('billaddress', '')
#         billcity = request.POST.get('billcity', '')
#         vehicle_id = request.POST.get('vehicle_id')
#         dayss = request.POST.get('dayss', '1')
#         date = request.POST.get('date', '')
#         location = request.POST.get('location', '')

#         # Get the vehicle (needed for bill.html)
#         vehicle = get_object_or_404(Vehicle, id=vehicle_id)

#         # Check for empty fields
#         if not billname or not billemail or not billphone or not billaddress or not billcity or not dayss or not date or not location:
#             messages.error(request, "All fields are required")
#             return render(request, 'bill.html', {
#                 'vehicle': vehicle,
#             })  # stays on same page

#         # Check if days is valid number
#         try:
#             duration = int(dayss)
#         except ValueError:
#             messages.error(request, "Invalid number of days.")
#             return render(request, 'bill.html', {
#                 'vehicle': vehicle,
#             })

#         total_amount = vehicle.price * duration

#         # Save booking
#         booking = Booking.objects.create(
#             vehicle=vehicle,
#             farmer=request.user,
#             booking_date=date,
#             duration=duration,
#             total_amount=total_amount
#         )

#         return render(request, 'confirmbooking.html', {'booking': booking})

#     return redirect('home')

 

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

# def search_vehicles(request):
#     query = request.GET.get('q', '')  # Get search query from request
#     if query:
#         vehicles = Vehicle.objects.filter(Vehicle_name__icontains=query)  # Use correct field name
#     else:
#         vehicles = Vehicle.objects.all()  # Show all vehicles when no search input

#     return render(request, 'vehicles.html', {'vehicles': vehicles, 'query': query})

  





# views.py
 

@login_required
def submit_rating(request):
    if request.method == "POST":
        try:
            vehicle_id = request.POST.get('vehicle_id')
            stars = request.POST.get('stars')
            print(f"Raw POST data: {request.POST}")

            if not stars:
                raise ValueError("Stars value is empty!")

            try:
                stars = int(stars)
                if stars < 1 or stars > 5:
                    raise ValueError("Stars must be between 1 and 5")
            except (ValueError, TypeError):
                return JsonResponse({'success': False, 'error': 'Invalid star value'})

            vehicle = Vehicle.objects.get(id=vehicle_id)

            # Use defaults to avoid NULL save
            rating_obj, created = Rating.objects.get_or_create(
                user=request.user,
                vehicle=vehicle,
                defaults={'stars': stars}
            )

            if not created:
                rating_obj.stars = stars
                rating_obj.save()

            # Update average rating
            all_ratings = Rating.objects.filter(vehicle=vehicle)
            total = sum(r.stars for r in all_ratings)
            count = all_ratings.count()
            vehicle.rating = total / count
            vehicle.num_ratings = count
            vehicle.save()

            return JsonResponse({'success': True, 'new_avg': vehicle.rating})

        except Exception as e:
            print("Error:", str(e))
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request'})


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
def delivery(request):
    return render(request,'delivery.html ')

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