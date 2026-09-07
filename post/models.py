from django.db import models
from django.contrib.auth.models import User

class post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    # author of post this column is foreignkey
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title
     