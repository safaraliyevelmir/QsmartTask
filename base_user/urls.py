from django.urls import path
from .views import *

urlpatterns = [
    path('login/',loginUser,name='login'),
    path('register/',register,name='register'),
    path('logout/',logoutUser,name='logout'),
    path('verify/<token>/',verify,name='verify'),

]
