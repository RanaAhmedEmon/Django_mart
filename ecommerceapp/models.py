from django.db import models  # Import Django models module to define database models

# Model for storing contact information
class Contact(models.Model):
    # Fields for name, email, description, and phone number
    name = models.CharField(max_length=50)  # CharField to store the name, max 50 characters
    email = models.EmailField()  # EmailField to store email addresses
    description = models.TextField(max_length=500)  # TextField for descriptions, max 500 characters
    phone = models.IntegerField()  # IntegerField to store phone numbers
    
    def __str__(self):
        return self.name  # Display name as the string representation of Contact

# Model for storing product details
class Product(models.Model):
    product_id = models.AutoField  # Auto-generated unique ID for each product
    product_name = models.CharField(max_length=100)  # Name of the product, max 100 characters
    category = models.CharField(max_length=100, default="")  # Main category of the product
    subcategory = models.CharField(max_length=50, default="")  # Subcategory of the product
    price = models.IntegerField(default=0)  # IntegerField to store the product's price
    description = models.CharField(max_length=300)  # Short description of the product, max 300 characters
    image = models.ImageField(upload_to='images/images')  # ImageField to upload and store product images
    inventory_quantity = models.PositiveIntegerField(default=0)  # PositiveIntegerField for stock quantity
    
    def __str__(self):
        return self.product_name  # Display product_name as the string representation of Product
