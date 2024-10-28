from django.shortcuts import render, redirect
from django.contrib.auth.models import User  # Import User model for user management
from django.contrib import messages  # Import messages for displaying feedback to users
from payment.models import Order  # Import Order model to retrieve user orders
from django.contrib.auth import authenticate, login, logout  # Import authentication functions

# View function to handle user signup
def signup(request):
    if request.method == "POST":
        # Retrieve email and password fields from the submitted form
        email = request.POST['email']
        password = request.POST['pass1']
        confirm_password = request.POST['pass2']
        
        # Check if passwords match
        if password != confirm_password:
            messages.warning(request, "Password not matched")
            return render(request, 'signup.html')  # Reload signup page if passwords don't match
        
        # Check if a user with the same email already exists
        try:
            if User.objects.get(username=email):
                messages.info(request, "Email already exists")
                return render(request, 'signup.html')
        
        except Exception as identifier:
            pass  # Ignore exception if user does not exist
        
        # Create and save new user if validation is successful
        user = User.objects.create_user(email, email, password)
        user.is_active = True
        user.save()
        return redirect('/auth/login/')  # Redirect to login page after signup
    
    return render(request, "signup.html")  # Render signup page for GET requests


# View function to handle user login
def handlelogin(request):
    if request.method == "POST":
        # Retrieve login credentials from the form
        username = request.POST['email']
        userpassword = request.POST['pass1']
        
        # Authenticate user based on provided credentials
        myuser = authenticate(username=username, password=userpassword)
        
        # Check if authentication is successful
        if myuser is not None:
            login(request, myuser)  # Log the user in
            messages.success(request, "Login Success")
            return redirect('/')  # Redirect to home page upon successful login
        else:
            messages.error(request, "Invalid Credentials")
            return redirect('/auth/login')  # Reload login page if authentication fails
        
    return render(request, 'login.html')  # Render login page for GET requests


# View function to handle user logout
def handlelogout(request):
    logout(request)  # Log the user out
    messages.info(request, "Logout Success")
    return redirect('/auth/login')  # Redirect to login page after logout


# View function to display the user's profile
def profile(request):
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        messages.warning(request, "Login & Try Again")
        return redirect('/auth/login')  # Redirect to login page if user is not logged in

    current_user = request.user  # Get the currently logged-in user
    orders = Order.objects.filter(user=current_user, ordered=True)  # Retrieve user's completed orders

    # Pass orders data to the template for display
    context = {
        'orders': orders,
    }
    
    return render(request, "profile.html", context)  # Render profile page with orders data
