from django.conf import settings
from django.db import models


class Action(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='actions', on_delete=models.CASCADE)
    verb = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]
