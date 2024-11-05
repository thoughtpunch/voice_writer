from django.urls import path
from voice_writer.views.user import login_user, logout_user, signup_user  # Import views from your app

urlpatterns = [
    path('login/', login_user, name='login'),
    path('signup/', signup_user, name='signup'),
    path('logout/', logout_user, name='logout'),
]
