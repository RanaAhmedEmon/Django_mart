from django.urls import path  # Import path for URL routing
from ecommerceapp import views  # Import views from the 'ecommerceapp' app

# Define URL patterns for the 'ecommerceapp' app
urlpatterns = [
    # URL pattern for the home page, mapped to the 'index' view
    path('', views.index, name="index"),
    
    # URL pattern for the contact page, mapped to the 'contact' view
    path('contact', views.contact, name="contact"),
    
    # URL pattern for the checkout page, mapped to the 'checkout' view
    path('checkout/', views.checkout, name='checkout'),
]
