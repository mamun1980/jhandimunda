from django.db import models
import time
from django.contrib.auth import get_user_model

User = get_user_model()


class Game(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False, unique=True)
    title = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(max_length=500, blank=True, null=True)
    banner = models.ImageField(upload_to='media/banner/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name


class Player(models.Model):
    player_id = models.CharField(max_length=10, primary_key=True, editable=False)
    user = models.OneToOneField(User, on_delete=models.RESTRICT, blank=False, null=False)

    def __str__(self) -> str:
        return self.player_id
    
    def save(self, *args, **kwargs):
        if not self.player_id:
            self.player_id =  int(time.time())
        super().save(*args, **kwargs)


class Agent(models.Model):
    agent_id = models.CharField(max_length=10, primary_key=True, editable=False)
    user = models.OneToOneField(User, on_delete=models.RESTRICT, blank=False, null=False)

    def __str__(self) -> str:
        return self.agent_id
    
    def save(self, *args, **kwargs):
        if not self.agent_id:
            self.agent_id = int(time.time())
        super().save(*args, **kwargs)
