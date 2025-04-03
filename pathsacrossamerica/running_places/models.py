from django.db import models

# Create your models here.
from django.db import models
PATH_TYPE_CHOICES = {
    "SO": "Soft",
    "GR": "Gravel",
    "DT": "Dirt",
    "HD": "Hard",
    "PV": "Paved",
    "CO": "Concrete",
}

TERRAIN_TYPE_CHOICES = {
    "FL": "Flat",
    "HL": "Hilly",
    "UN": "Uneven",
}

class RunningPlace(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    description = models.TextField()
    path_type = models.CharField(max_length=2, choices=PATH_TYPE_CHOICES.items(), default="SOFT")
    terrain_type = models.CharField(max_length=2, choices=TERRAIN_TYPE_CHOICES.items(), default="FLAT")
    length = models.IntegerField()

    def __str__(self):
        return str(self.id) + ' - ' + self.name