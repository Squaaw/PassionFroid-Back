from django.db import models
from image.models import Image

# Create your models here.
class Tags(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    image = models.ForeignKey(Image, on_delete = models.CASCADE, blank = False, null = False)

    def __str__(self):
        return self.name