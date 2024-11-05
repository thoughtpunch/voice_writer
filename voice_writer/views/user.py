# voice_writer/views/user.py
from django.shortcuts import render, redirect
from django.contrib import messages
from supabase import create_client, Client
from django.conf import settings
from voice_writer.models.user import User

# Initialize Supabase client
supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)


def signup_user(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')

        if not email or not password:
            messages.error(request, "Email and password are required.")
            return render(request, 'voice_writer/user/signup.html')

        try:
            # Sign up the user with Supabase
            response = supabase.auth.sign_up({
                'email': email,
                'password': password,
                'options': {
                    'data': {
                        'first_name': first_name,
                        'last_name': last_name
                    }
                }
            })

            if response.user:
                # Create a Django user if Supabase signup is successful
                user = User.objects.create_user(
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name
                )
                login(request, user)  # Automatically log in the new user
                messages.success(request, "Signup successful!")
                return redirect('home')  # Redirect to the home page after signup
            else:
                messages.error(request, "Signup failed. Please try again.")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

    return render(request, 'voice_writer/user/signup.html')


def login_user(request):
    """
    Log in an existing user by authenticating with Supabase and creating a Django session.
    """
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        # Authenticate with Supabase
        try:
            response = supabase.auth.sign_in_with_password(email=email, password=password)
            if response.get('error'):
                # Handle login error
                return render(request, 'voice_writer/user/login.html', {'error': response['error']['message']})
        except Exception as e:
            return render(request, 'voice_writer/user/login.html', {'error': str(e)})

        # Retrieve or create the user in Django's database
        user, created = User.objects.get_or_create(email=email)
        if created:
            user.set_password(password)  # Only save password locally if needed
            user.save()

        # Log in the user with Django's session management
        login(request, user)
        return redirect('home')  # Redirect to the home page after login

    return render(request, 'voice_writer/user/login.html')  # Render login page if GET request


def logout_user(request):
    """
    Log out the user from both Supabase and Django.
    """
    # Supabase logout
    try:
        supabase.auth.sign_out()
    except Exception as e:
        # Optionally handle Supabase sign-out errors
        pass

    # Django logout
    logout(request)
    return redirect('login')  # Redirect to login page after logout
