from django.urls import include, path
from .views import login_view, logout_view

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]

# HEALTH CHECK
urlpatterns += [
    path(r'ht/', include('health_check.urls'))
]
