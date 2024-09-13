from django.db import models
from falco.models import TimeStamped

class Post(TimeStamped):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)