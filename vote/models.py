from django.db import models
from acc.models import User
# Create your models here.

class Topic(models.Model):
    subject = models.CharField(max_length=100)
    writer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="vwriter")  # 참고해야하는게 2개 이상일 경우 related_name 주기  # vwriter : 유저가 사용하는 이름
    pubdate = models.DateTimeField()
    content = models.TextField()
    voter = models.ManyToManyField(User, blank=True, related_name="voter")

    def __str__(self):
        return self.subject

    def summary(self):      # 요약
        if len(self.content) > 10:
            return self.content[:10] + "..."
        return self.content

    # 레코드 == 객체 (django에서 orm 뭔지 생각하기)

class Choice(models.Model):
    subject = models.ForeignKey(Topic, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)         # 이미지 투표라서 Charfield
    pic = models.ImageField(upload_to="vote/%y/%m") # 년(%y) 월(%m) 일(%d)
    comment = models.TextField()
    choicer = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return f"{self.subject}-{self.name}"
