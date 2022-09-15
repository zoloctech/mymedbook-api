from django.db import models
from users.models import User

# Create your models here.

class Order(models.Model):
    user =  models.ForeignKey(User, on_delete=models.CASCADE)
    order_amount = models.CharField(max_length=25)
    order_payment_id = models.CharField(max_length=100)
    isPaid = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user + ' ' + self.order_amount 