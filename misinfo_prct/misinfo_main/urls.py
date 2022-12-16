from django.urls import path

from misinfo_prct.misinfo_main import views

app_name = 'misinfo_main'
urlpatterns = [
    path('', views.home, name='home'),
    ]