from django.contrib import admin
from django.urls import path
from Agrivehicles import views

urlpatterns = [
    path("", views.index, name='home'),
    path("home/", views.index, name='home'),
    path("about", views.about, name='about'),

    # Vehicle management (Owner)
    path("add-vehicle/", views.add_vehicle, name='add_vehicle'),
    path("delete-vehicle/<int:id>/", views.delete_vehicle, name='delete_vehicle'),

    # Owner Bookings
    path("bookings", views.owner_bookings, name='owner_bookings'),
    path("delete-booking/<int:id>/", views.delete_booking, name='delete_booking'),

    # Vehicle listings (General view for all users)
    path("vehicles", views.vehicles, name="vehicles"),

    # Farmer Bookings
    path("my-bookings/", views.farmer_bookings, name='farmer_bookings'),
    path('farmer/bookings/delete/<int:id>/', views.delete_farmer_booking, name='delete_farmer_booking'),


    # Authentication
    path("register", views.register, name="register"),
    path("signin", views.signin, name="signin"),
    path("signout", views.signout, name="signout"),

    # Billing & Orders
    path("bill/<int:id>/", views.bill, name='bill'),  # vehicle_id renamed to id
    path("order/", views.order, name='order'),
    path("confirmbooking", views.confirmbooking, name='confirmbooking'),

    # Contact
    path("contact", views.contact, name='contact'),
    path('all-messages/', views.all_messages, name='all_messages'),

    # Ratings & Reviews
    path("submit-rating/", views.submit_rating, name='submit_rating'),
    path("submit-review/", views.submit_review, name='submit_review'),
    path("get-reviews/<int:id>/", views.get_reviews, name='get_reviews'),

    # Profile
    path("update-profile/", views.update_profile, name='update_profile'),
    path("get-user-role/", views.get_user_role, name='get_user_role'),
]
