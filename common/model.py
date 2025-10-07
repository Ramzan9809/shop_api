from django.db import models
# from django.utils import timezone

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True) # default=timezone.now()

    class Meta:
        abstract = True