from django.db import models


# Create your models here.
class FirstApp(models.Model):
    order_id = models.IntegerField(unique=True)
    price_dollars = models.IntegerField()
    price_rubles = models.IntegerField()
    delivery_time = models.DateField()