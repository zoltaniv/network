from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    
    def __str__(self):
        if not self.first_name or not self.last_name:
            return f"{self.username}"
        return f"{self.first_name} {self.last_name}"


class Post(models.Model):
    
    text = models.TextField(
        max_length=264, verbose_name="")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE , 
        related_name="myposts")
    date = models.DateTimeField(auto_now_add= True)
    
    def __str__(self):
        return f"{self.author}'s post, from {self.date}"
    
    
class Like(models.Model):
    
    post = models.ForeignKey(
        Post, on_delete= models.CASCADE,
        related_name= "plikes")
    author = models.ForeignKey(
        User, on_delete= models.CASCADE,
        related_name= "mylikes")
    date = models.DateTimeField(auto_now_add= True)
    
    def __str__(self):
        return f"{self.author}'s like, from {self.date}"
    

class Subscription(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, 
                                 related_name="subscriptions")
    subscribers = models.ManyToManyField(User, related_name="followers")
    
    def __str__(self):
        return f"{self.follower}: subscription object"
    
    