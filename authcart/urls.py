from django.urls import path
from authcart import views  # Import views from the 'authcart' app

# Define URL patterns for the 'authcart' app
urlpatterns = [
    # URL pattern for the signup page
    path('signup/', views.signup, name='signup'),
    
    # URL pattern for the login page
    path('login/', views.handlelogin, name='handlelogin'),
    
    # URL pattern for logging out the user
    path('logout/', views.handlelogout, name='handlelogout'),
    
    # URL pattern for the user profile page
    path('profile/', views.profile, name='profile'),
]
