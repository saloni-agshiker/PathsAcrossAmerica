from django.db import models
from django.contrib.auth.models import User

class Review(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    running_place = models.ForeignKey('running_places.RunningPlace', on_delete=models.CASCADE)
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    def __str__(self):
        return str(self.id) + ' - ' + self.running_place.name

# need to FULLY define the below model eventually
class RunningPlace(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)