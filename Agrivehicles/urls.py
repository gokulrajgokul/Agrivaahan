from django.contrib import admin
from django.urls import path
 
from Agrivehicles import views

urlpatterns = [
    path("",views.index, name = 'home'),
    path("home/",views.index, name = 'home'),
    path("about",views.about,name = 'about'),
    path('add-vehicle', views.add_vehicle, name='add_vehicle'),
    # path('add-vehicle/', views.add_vehicle, name='add_vehicle'),
    path('delete-vehicle/<int:pk>/', views.delete_vehicle, name='delete_vehicle'),
    path('bookings', views.owner_bookings, name='owner_bookings'),
    path('delete-booking/<int:booking_id>/', views.delete_booking, name='delete_booking'),
    path("vehicles", views.vehicles, name= "vehicles"),
    path('my-bookings/', views.farmer_bookings, name='farmer_bookings'),
    path('delete-my-booking/<int:booking_id>/', views.delete_farmer_booking, name='delete_farmer_booking'),
    path("register", views.register, name="register"),
    path("signin", views.signin, name="signin"),
    path("signout",views.signout,name = "signout"),
    path('bill/<int:vehicle_id>/', views.bill, name='bill'),
    path('order/', views.order, name='order'),
    path("contact",views.contact,name = 'contact'),
    # path('search/', views.search_vehicles, name='search_vehicles'),
    path('submit-rating/', views.submit_rating, name='submit_rating'),
    path('confirmbooking', views.confirmbooking, name='confirmbooking'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path("delivery",views.delivery,name = 'delivery'),
    path('get-user-role/', views.get_user_role, name='get_user_role')

    

    ]

 