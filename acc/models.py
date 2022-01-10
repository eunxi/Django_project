from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    age = models.IntegerField(default=0)
    comment = models.TextField()
    pic = models.ImageField()
    
    def getpic(self):
        if self.pic:
            return self.pic.url
        else:
            return "/media/noimage.png"