from django.db import models
import uuid
# Create your models here.
class Author(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField()
    bio = models.TextField()
    host = models.URLField()
    firstName = models.CharField(max_length=256)
    lastName = models.CharField(max_length=256)
    displayName = models.CharField(max_length=256)
    url = models.URLField()
    github = models.URLField()


