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
class Review(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    running_place = models.ForeignKey('running_places.RunningPlace', on_delete=models.CASCADE)
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    def __str__(self):
        return str(self.id) + ' - ' + self.running_place.name

class RunningPlace(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    description = models.TextField()
    path_type = models.CharField(max_length=2, choices=PATH_TYPE_CHOICES.items(), default="Gravel")
    terrain_type = models.CharField(max_length=2, choices=TERRAIN_TYPE_CHOICES.items(), default="Flat")
    length = models.IntegerField()

    def __str__(self):
        return str(self.id) + ' - ' + self.name