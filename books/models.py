
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

def validate_mail(value):
    if "@gmail.com" in value:
        return value
    else:
        raise ValidationError("This mail is not valid!!")


class Book(models.Model):
    title  = models.CharField(max_length = 200)
    author = models.CharField(max_length = 200)
    description = models.CharField(max_length = 500, default=None)
    price = models.FloatField(null=True, blank=True)
    image = models.ImageField(upload_to="book",null=True)
    book_available = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, default=None)
    seller=models.CharField(max_length=100,null=True)
    seller_contact=models.CharField(max_length=100,null=True)
    seller_email=models.CharField(max_length=100,null=True)

    def __str__(self):
        return self.title



class Order(models.Model):
	product = models.ForeignKey(Book, max_length=200, null=True, blank=True, on_delete = models.SET_NULL)
	created =  models.DateTimeField(auto_now_add=True) 

	def __str__(self):
		return self.product.title

class Contact(models.Model):
    name=models.CharField(max_length = 200)
    email=models.CharField(max_length = 200)
    request=models.CharField(max_length = 200)

    def __str__(self):
        return self.name