from django.db import models
from acc.models import User

# Create your models here.
class Book(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="book")
    site_name = models.CharField(max_length=100)
    site_url = models.TextField()
    comment = models.TextField()
    impo = models.BooleanField()    # 중요한 site 는 체크, 아니면 해제해주는 field

    def __str__(self):
        return self.site_namemys