from django.db import models
from django.contrib.auth.models import User

class Order(models.Model):
    # Link order to a user; deleting user deletes associated orders
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Store items in JSON format, with a limit of 5000 characters
    items_json = models.CharField(max_length=5000)
    
    # Customer's name, up to 90 characters
    name = models.CharField(max_length=90)

    # Order amount with max of 10 digits, 2 after decimal for currency format
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    # Customer's email, max 90 characters
    email = models.CharField(max_length=90)

    # Primary address field, up to 200 characters
    address1 = models.CharField(max_length=200)

    # City name, up to 100 characters
    city = models.CharField(max_length=100)

    # Zip code, default is '00000', max length of 10 characters
    zip_code = models.CharField(max_length=10, default='00000')   

    # Phone number, with default empty string and max 100 characters
    phone = models.CharField(max_length=100, default="")

    # Track whether the order has been completed
    ordered = models.BooleanField(default=False)

    # Automatically add timestamp when the order is created
    created_at = models.DateTimeField(auto_now_add=True)

    # String representation to easily identify orders
    def __str__(self):
        return f"{self.name} - {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
