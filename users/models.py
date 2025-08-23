from django.db import models


class User(models.Model):
    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, blank=True)
    user_name = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    hashed_password = models.TextField()
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} {self.last_name} | {self.user_name} | {self.email} | {self.registered_at}"