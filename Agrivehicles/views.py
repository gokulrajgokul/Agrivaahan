from django.http import Http404, HttpResponse
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import Vehicle, Order, Contact ,UserProfile,Rating,Booking
from django.http import JsonResponse 
from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request):
	return render(request,'index.html')
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


from .models import UserProfile  # make sure this import exists

def signin(request):
    if request.method == "POST":
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        user = authenticate(username=loginusername, password=loginpassword)
        if user is not None:
            login(request, user)

            try:
                user_profile = UserProfile.objects.get(user=user)
                if user_profile.role == 'owner':
                    return redirect('home')  # Owner → Add Vehicle page
                else:
                    return redirect('vehicles')  # Farmer → View Vehicles page
            except UserProfile.DoesNotExist:
                messages.error(request, "User profile not found.")
                return redirect('signin')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('signin')

    else:
        return render(request, 'login.html')


def signout(request):
        logout(request)
        # messages.success(request,"Successfully logged out!")
        return redirect('signin')
    
    # return HttpResponse('signout')

from django.contrib.auth.decorators import login_required
from .models import Vehicle

@login_required
def add_vehicle(request):
    if request.method == 'POST':
        name = request.POST.get('Vehicle_name')
        desc = request.POST.get('Vehicle_desc')
        price = request.POST.get('price')
        image = request.FILES.get('image')

        Vehicle.objects.create(
            Vehicle_name=name,
            Vehicle_desc=desc,
            price=price,
            image=image,
            owner=request.user 
        )

        messages.success(request, "Vehicle added successfully!")
        return redirect('add_vehicle')  # or anywhere you want

    return render(request, 'add_vehicle.html')

@login_required
def owner_bookings(request):
    # Fetch the logged-in user
    owner = request.user
    
    # Fetch all bookings for the vehicles owned by this user
    bookings = Booking.objects.filter(vehicle__owner=owner)
    
    # Add a debug print to check if bookings are being fetched
    print("Owner:", owner)
    print("Bookings:", bookings)

    return render(request, 'bookings.html', {'bookings': bookings})

def vehicles(request):
    Vehicles = Vehicle.objects.all()
    # print(cars)
    params = {'Vehicle':Vehicles}
    return render(request,'vehicles.html',params)

# def bill(request):
#     Vehicles= Vehicle.objects.all()
#     params = {'vehicles':Vehicles}
#     return render(request,'bill.html',params)
 
def bill(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    return render(request, 'bill.html', {'vehicle': vehicle})



# def order(request):
#     if request.method == "POST":
#         billname = request.POST.get('billname','')
#         billemail = request.POST.get('billemail','')
#         billphone = request.POST.get('billphone','')
#         billaddress = request.POST.get('billaddress','')
#         billcity = request.POST.get('billcity','')
#         cars11 = request.POST['cars11']
#         dayss = request.POST.get('dayss','')
#         date = request.POST.get('date','')
#         fl = request.POST.get('fl','')
#         tl = request.POST.get('tl','')
#         # print(request.POST['cars11'])
        
#         order = Order(name = billname,email = billemail,phone = billphone,address = billaddress,city=billcity,cars = cars11,days_for_rent = dayss,date = date,loc_from = fl,loc_to = tl)
#         order.save()
#         return redirect('home')
#     else:
#         print("error")
#         return render(request,'bill.html')




 

def order(request):
    if request.method == "POST":
        billname = request.POST.get('billname', '')
        billemail = request.POST.get('billemail', '')
        billphone = request.POST.get('billphone', '')
        billaddress = request.POST.get('billaddress', '')
        billcity = request.POST.get('billcity', '')
        vehicle_id = request.POST.get('vehicle_id')
        dayss = request.POST.get('dayss', '')
        date = request.POST.get('date', '')
        location = request.POST.get('location', '')  # ✅ Combined location field

        vehicle = get_object_or_404(Vehicle, id=vehicle_id)

        order = Order(
            name=billname,
            email=billemail,
            phone=billphone,
            address=billaddress,
            city=billcity,
            vehicle_name=vehicle.Vehicle_name,  # ✅ This will store the vehicle name
            days_for_rent=int(dayss),
            date=date,
            location=location,  # ✅ Using the single combined location
        )
        order.save()

        return redirect('home')

    return redirect('home')


def contact(request):
    if request.method == "POST":
        contactname = request.POST.get('contactname','')
        contactemail = request.POST.get('contactemail','')
        contactnumber = request.POST.get('contactnumber','')
        contactmsg = request.POST.get('contactmsg','')

        contact = Contact(name = contactname, email = contactemail, phone_number = contactnumber,message = contactmsg)
        contact.save()
    return render(request,'contact.html ')

def search_vehicles(request):
    query = request.GET.get('q', '')  # Get search query from request
    if query:
        vehicles = Vehicle.objects.filter(Vehicle_name__icontains=query)  # Use correct field name
    else:
        vehicles = Vehicle.objects.all()  # Show all vehicles when no search input

    return render(request, 'vehicles.html', {'vehicles': vehicles, 'query': query})



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
