from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Vehicle(models.Model):
    

    Vehicle_id = models.IntegerField(default=0, unique=True)
    Vehicle_name = models.CharField(max_length=30,default="")
    Vehicle_desc = models.CharField(max_length=300,default="")
    price = models.IntegerField(default=0)
    image = models.ImageField(upload_to="Vehicle/images",default="")
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    owner_location=models.CharField(max_length=100 ,default="")
    is_available = models.BooleanField(default=True)
    rating = models.FloatField(default=0.0)         # Average rating
    num_ratings = models.IntegerField(default=0)  # Number of ratings
    
    delivery_time_0_10 = models.CharField(max_length=50, blank=True, null=True)
    delivery_time_10_20 = models.CharField(max_length=50, blank=True, null=True)
   



    def save(self, *args, **kwargs):
        if self.Vehicle_id == 0 or self.Vehicle_id is None:
            last_id = Vehicle.objects.aggregate(models.Max('Vehicle_id'))['Vehicle_id__max'] or 0
            self.Vehicle_id = last_id + 1
        super().save(*args, **kwargs)


    def __str__(self):
        return self.Vehicle_name
class Rating(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='ratings',  to_field='Vehicle_id')  # 👈 Fix here
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField(choices=[(i, i) for i in range(1, 6)],null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('vehicle', 'user')

    def __str__(self):
        return f"{self.user.username} rated {self.vehicle.Vehicle_name} {self.stars} stars"


# class Order(models.Model) :
#     order_id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=90,default="")
#     email = models.CharField(max_length=50,default="")
#     phone = models.CharField(max_length=20,default="")
#     address = models.CharField(max_length=500,default="")
#     city = models.CharField(max_length=50,default="")
#     cars = models.CharField(max_length=50,default="")
#     days_for_rent = models.IntegerField(default=0)
#     date = models.CharField(max_length=50,default="")
#     loc_from = models.CharField(max_length=50,default="")
#     loc_to = models.CharField(max_length=50,default="")
    
#     def __str__(self):
#         return self.name



class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=90, default="")
    email = models.CharField(max_length=50, default="")
    phone = models.CharField(max_length=20, default="")
    address = models.CharField(max_length=500, default="")
    city = models.CharField(max_length=50, default="")
    vehicle_name = models.CharField(max_length=50, default="")  # Rename to vehicle_name if you want
    days_for_rent = models.IntegerField(default=0)
    date = models.CharField(max_length=50, default="")
    location = models.CharField(max_length=50, default="")  # 🔁 NEW field replacing loc_from + loc_to

    def __str__(self):
        return self.name


class Contact(models.Model):
    message = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150,default="")
    email = models.EmailField(max_length=150,default="")   
    phone_number = models.CharField(max_length=15,default="")
    message = models.TextField(max_length=500,default="")
 

    def __str__(self) :
        return self.name
 

    
# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)  
#     phone = models.CharField(max_length=15)  
#     email = models.EmailField(unique=True)  # Store email separately  
     

#     def __str__(self):
#         return self.user.username
 

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('farmer', 'Farmer'),
        ('owner', 'Vehicle Owner'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)  
    phone = models.CharField(max_length=15)  
    email = models.EmailField(unique=True)  
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)  # New field

    def __str__(self):
        return f"{self.user.username} ({self.role})"

class Booking(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    farmer = models.ForeignKey(User, on_delete=models.CASCADE)  # person who booked
    booking_date = models.DateField()
    duration = models.IntegerField()
    total_amount = models.FloatField()
    visible_to_farmer = models.BooleanField(default=True)
    visible_to_owner = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now) 

    def __str__(self):
        return f"{self.vehicle.Vehicle_name} booked by {self.farmer.username}"
class VehicleReview(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
       return f"{self.user.username} rated {self.vehicle.Vehicle_name} {self.rating} stars - '{self.review[:30]}...'"
