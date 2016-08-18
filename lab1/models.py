from django.db import models
from django.utils import timezone

class URL(models.Model):
    originalURL = models.URLField(max_length=300,null=True)
    statusCode = models.CharField(max_length=3, default='200')
    title = models.TextField(max_length=50, null=True)
    finalDestination = models.URLField(max_length=300,null=originalURL)
    datetime = models.CharField(max_length=50, null=True)
    wayback = models.CharField(max_length=300, null=originalURL)
    wayback_date = models.CharField(max_length=50, null=True)
    archive = models.CharField(max_length=300, null=True)
    
    def __str__(self):
        return self.originalURL
