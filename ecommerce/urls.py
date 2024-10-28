"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin  # Import Django's admin module
from django.urls import path, include  # Import path and include for URL routing
from django.conf.urls.static import static  # Import static for serving media files
from django.conf import settings  # Import settings to access project configurations

# Define the URL patterns for the ecommerce project
urlpatterns = [
    # Admin route for accessing the Django admin site
    path('admin/', admin.site.urls),
    
    # Include URLs from the 'ecommerceapp' app, setting it as the homepage
    path('', include("ecommerceapp.urls")),
    
    # Include URLs for user authentication (signup, login, logout) from 'authcart' app
    path('auth/', include("authcart.urls")),
    
    # Include URLs for handling payments from the 'payment' app
    path('payment/', include("payment.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Serve media files during development
