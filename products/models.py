from django.db import models
from datetime import datetime


class Product(models.Model):

    name = models.CharField(max_length=100)
    content = models.TextField()
    is_active = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    photo = models.ImageField(upload_to='photo/%y/%m/%d')
    publish_date = models.DateTimeField(default=datetime.now)

    def __str__(self):

        return self.name

    class Meta:
        ordering = ['-publish_date']