from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    email = models.CharField(max_length=60)

    def __str__(self):
        return self.username

class Center(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    address = models.CharField(max_length=250)
    
    def get_slots_count(self):
        return self.slot_set.filter(name=self, username=None).count()
    
    def __str__(self):
        return self.name
    

class Slot(models.Model):
    name = models.ForeignKey(Center,on_delete=models.CASCADE, default=None)
    timings = models.CharField(max_length=50)
    username = models.ForeignKey(User,on_delete=models.CASCADE, default=None, blank=True, null=True)
