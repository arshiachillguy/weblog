from django.db import models

class user(models.Model):
     username = models.TextField()
     email = models.TextField()

