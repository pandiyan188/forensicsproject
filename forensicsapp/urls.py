from django.urls import path
from .import views

urlpatterns = [
    path('',views.home, name='home'),
    path('home',views.home, name='home'),
    path('signin',views.signin,name='signin'),
    path('signup',views.signup,name='signup'),
    path('predict',views.predict,name='predict')
]