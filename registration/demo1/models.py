from django.db import models
from django.contrib.auth.models import User

CATEGORY_CHOICES = (
    ('ST','Starters'),
    ('MC','Main Course'),
    ('DS','Dessert'),
    ('DK','Drinks'),
)


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete = models.CASCADE)
    mobile = models.CharField(max_length = 20)
    otp = models.CharField(max_length = 6)


class Product(models.Model):
    title = models.CharField(max_length = 100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    composition = models.TextField(default = '')
    prodapp = models.TextField(default = '')
    category = models.CharField(choices = CATEGORY_CHOICES,max_length = 2)
    product_image = models.ImageField(upload_to = 'product')

    def _str_(self):
        return self.title


class Cart(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    product = models.ForeignKey(Product,on_delete = models.CASCADE)
    quantity = models.PositiveIntegerField(default = 1)

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price
