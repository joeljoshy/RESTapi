from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Article(models.Model):

    title = models.CharField(max_length=120)
    author = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    email=models.EmailField(max_length=120)
    date = models.DateTimeField(auto_now_add=True)


    def __str__(self):

        return self.title