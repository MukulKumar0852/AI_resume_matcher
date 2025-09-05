from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),                   # Homepage route
    path('home/', views.home, name='home_page'),         # /home route
    path('match/', views.match_resume, name='match'), # /match route
    
]
