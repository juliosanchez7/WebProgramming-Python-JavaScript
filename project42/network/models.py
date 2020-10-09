from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
class Post(models.Model):
    content=models.TextField(blank=True)
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts")
    
    timestamp = models.DateTimeField(auto_now_add=True)
    def serialize(self):
        return{
            "id": self.id,
            "user": self.user.username,
            "timestamp": self.timestamp.strftime("%b %-d %Y, %-I:%M %p"),
            "content": self.content,
            
        }
