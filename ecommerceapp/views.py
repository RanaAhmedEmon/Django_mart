from django.shortcuts import render, redirect
from ecommerceapp.models import Contact, Product
from django.contrib import messages
from math import ceil
from django.conf import settings
import json
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from payment.models import Order

# View for the homepage
def index(request):
    allProds = []  # List to store all products categorized by their category
    catprods = Product.objects.values('category', 'id', 'inventory_quantity')  # Retrieve category, id, and inventory
    cats = {item['category'] for item in catprods}  # Extract unique categories

    # Loop through each category to retrieve and organize products for display
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)  # Number of products in this category
        nSlides = n // 4 + ceil((n / 4) - (n // 4))  # Calculate number of slides needed for display
        allProds.append([prod, range(1, nSlides), nSlides])

    params = {'allProds': allProds}  # Context for template rendering
    return render(request, "index.html", params)


# View for handling contact form submissions
def contact(request):
    if request.method == "POST":
        # Retrieve data from the form
        name = request.POST.get("name")
        email = request.POST.get("email")
        description = request.POST.get("description")
        phone = request.POST.get("phone")
        
        # Create a new contact entry and save to the database
        myquery = Contact(name=name, email=email, description=description, phone=phone)
        myquery.save()
        
        # Inform the user of successful submission
        messages.info(request, "We will get back to you soon..")
        return render(request, "contact.html")

    return render(request, "contact.html")


# View for checkout process, requires user to be logged in
@login_required
def checkout(request):
    # Redirect user to login page if they are not logged in
    if not request.user.is_authenticated:
        messages.warning(request, "Please log in to proceed with the checkout.")
        return redirect('/auth/login')

    # Handle form submission for order processing
    if request.method == "POST":
        # Retrieve order details from form data
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amt', '0')
        email = request.POST.get('email', '')
        address1 = request.POST.get('address1', '')
        city = request.POST.get('city', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')

        # Convert amount to Decimal for accurate handling of monetary values
        try:
            amount = Decimal(amount)
        except (ValueError):
            # Inform the user if the amount format is incorrect
            messages.error(request, "Invalid amount format.")
            return redirect('/checkout/')
        
        # Create and save the order in the database
        order = Order(user=request.user, items_json=items_json, name=name, amount=amount, zip_code=zip_code,
                      email=email, address1=address1, city=city, phone=phone)
        order.save()
        
        # Update product inventory based on items in the order
        cart = json.loads(items_json)  # Parse JSON cart data
        for item_id, details in cart.items():
            product_id = item_id.lstrip('pr')  # Strip 'pr' prefix from product ID
            qty_ordered = details[0]  # Quantity ordered of this product

            try:
                # Retrieve the product and update inventory if enough stock is available
                product = Product.objects.get(id=product_id)
                if product.inventory_quantity >= qty_ordered:
                    product.inventory_quantity -= qty_ordered  # Deduct ordered quantity
                    product.save()  # Save updated inventory
                else:
                    # Inform the user if there is insufficient stock
                    messages.error(request, f"Not enough stock for product {product.product_name}.")
                    return redirect('cart')
            except Product.DoesNotExist:
                # Inform the user if the product does not exist
                messages.error(request, f"Product with id {product_id} does not exist.")
                return redirect('cart')

        # Redirect to the payment page after successful order processing
        return redirect('payment:payment')
    
    # Render the checkout page if the request is not a POST
    return render(request, 'checkout.html')
