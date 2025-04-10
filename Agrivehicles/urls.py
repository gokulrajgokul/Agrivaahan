from django.contrib import admin
from django.urls import path

from Agrivehicles import views

urlpatterns = [
    path("",views.index, name = 'home'),
    path("home/",views.index, name = 'home'),
    path("about",views.about,name = 'about'),
    path('add-vehicle', views.add_vehicle, name='add_vehicle'),
    path('bookings', views.owner_bookings, name='owner_bookings'),
    path("vehicles", views.vehicles, name= "vehicles"),
    path("register", views.register, name="register"),
    path("signin", views.signin, name="signin"),
    path("signout",views.signout,name = "signout"),
    path('bill/<int:vehicle_id>/', views.bill, name='bill'),
    path('order/', views.order, name='order'),

    path("contact",views.contact,name = 'contact'),
    path('search/', views.search_vehicles, name='search_vehicles'),
    path('submit-rating/', views.submit_rating, name='submit_rating'),

    

    ]