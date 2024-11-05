from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from voice_writer.views.author import author_profile, update_author
from voice_writer.views.base import index
from voice_writer.views.user import login_user, logout_user, signup_user
from voice_writer.views.voice import (create_voice_recording,
                                      edit_voice_recording,
                                      voice_recording_list)

# HTML
urlpatterns = [
    path('', index, name='index'),
    path('users/signup/', signup_user, name='signup'),
    path('users/login/', login_user, name='login'),
    path('users/logout/', logout_user, name='logout'),
    path('recordings/', voice_recording_list, name='voice_recording_list'),
    path('recordings/edit/<uuid:id>/', edit_voice_recording, name='edit_voice_recording'),
    path('recordings/new/', create_voice_recording, name='create_voice_recording'),
    path('author/', author_profile, name='author_profile'),
    path('author/', update_author, name='update_author'),
]