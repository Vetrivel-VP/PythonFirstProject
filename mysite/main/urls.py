from django.urls import path
from . import views


app_name = 'main'  # here for namespacing of urls.

urlpatterns = [
    path("/", views.indexpage, name="indexpage"),
    path("index/",views.indexpage, name="indexpage"),
    path("aboutus/",views.aboutuspage, name="aboutuspage"),
    path("contactus/",views.contactuspage, name="contactuspage"),
    path("account/",views.accountspage, name="accountpage"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout_request, name="logout"),
     path("login/", views.login_request, name="login"),
     path("<single_slug>", views.single_slug, name="single_slug"),
]