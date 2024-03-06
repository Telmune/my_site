from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=100)
    price = models.IntegerField()
    descriptions = models.CharField(max_length=250)

    def __str__(self):
        return self.title
