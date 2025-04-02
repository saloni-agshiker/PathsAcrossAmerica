from django.db import models

# Create your models here.
from django.db import models
PATH_TYPE_CHOICES = {
    "SOFT": "SO",
    "GRAVEL": "GR",
    "DIRT": "DT",
    "HARD": "HD",
    "PAVED": "PV",
    "CONCRETE": "CO",
}

TERRAIN_TYPE_CHOICES = {
    "FLAT": "FL",
    "HILLY": "HL",
    "UNEVEN": "UN",
}

class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    description = models.TextField()
    path_type = models.CharField(max_length=8, choices=PATH_TYPE_CHOICES.items(), default="SOFT")
    terrain_type = models.CharField(max_length=6, choices=TERRAIN_TYPE_CHOICES.items(), default="FLAT")
    length = models.IntegerField()

    image = models.ImageField(upload_to='movie_images/')
    def __str__(self):
        return str(self.id) + ' - ' + self.name