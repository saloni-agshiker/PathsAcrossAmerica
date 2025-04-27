from django.db import models
from django.contrib.auth.models import User

# Create your models here.
PATH_TYPE_CHOICES = {
    "GR": "Gravel",
    "DT": "Dirt",
    "PV": "Paved",
    "CO": "Concrete",
}

TERRAIN_TYPE_CHOICES = {
    "FL": "Flat",
    "HL": "Hilly",
}

PARKING_CHOICES = {
    "FR": "Free",
    "PA": "Paid",
}

RESTROOM_CHOICES = {
    "Y": "Yes",
    "N": "No",
}

class RunningPlace(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    description = models.TextField()
    path_type = models.CharField(max_length=2, choices=PATH_TYPE_CHOICES.items(), default="Gravel")
    terrain_type = models.CharField(max_length=2, choices=TERRAIN_TYPE_CHOICES.items(), default="Flat")
    length = models.IntegerField()
    parking = models.CharField(max_length=2, choices=PARKING_CHOICES.items(), default="Free")
    restroom = models.CharField(max_length=2, choices=RESTROOM_CHOICES.items(), default="Yes")
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return str(self.id) + ' - ' + self.name

class Review(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    running_place = models.ForeignKey(RunningPlace, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.id) + ' - ' + self.running_place.name