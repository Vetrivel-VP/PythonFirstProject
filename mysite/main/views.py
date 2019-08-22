from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse
from . models import Tutorial, TutorialCategory, TutorialSeries
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from .forms import NewUserForm
from django.core.mail import send_mail
# Create your views here.


def single_slug(request, single_slug):
    # first check to see if the url is in categories.

    categories = [c.category_slug for c in TutorialCategory.objects.all()]
    if single_slug in categories:
        matching_series = TutorialSeries.objects.filter(tutorial_category__category_slug=single_slug)
        series_urls = {}

        for m in matching_series.all():
            part_one = Tutorial.objects.filter(tutorial_series__tutorial_series=m.tutorial_series).earliest("tutorial_published")
            series_urls[m] = part_one.tutorial_slug

        return render(request=request,
                      template_name='main/category.html',
                      context={"tutorial_series": matching_series, "part_ones": series_urls})

    tutorials =[t.tutorial_slug for t in Tutorial.objects.all()]
    if single_slug in tutorials:
        this_tutorial = Tutorial.objects.get(tutorial_slug=single_slug)
        tutorials_from_series = Tutorial.objects.filter(tutorial_series__tutorial_series=this_tutorial.tutorial_series).order_by('tutorial_published')
        this_tutorial_idx = list(tutorials_from_series).index(this_tutorial)

        return render(request = request,
                      template_name='main/tutorial.html',
                      context = {"tutorial":this_tutorial,
                                 "sidebar":tutorials_from_series,
                                 "this_tutorial_idx":this_tutorial_idx})

    return HttpResponse(f"{single_slug} does not  corresponds to anything")

def indexpage(request):
    return render(request = request,
                  template_name='main/home.html',
                  context={"categories": TutorialCategory.objects.all})

def aboutuspage(request):
    return render(request = request,
                  template_name='main/aboutus.html',
                  context={"categories": TutorialCategory.objects.all})
    
def contactuspage(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        from_email = request.POST.get('from_email')
        msg = request.POST.get('message')
        admin_mail = settings.EMAIL_HOST_USER
        message = "\tFirst Name:" + first_name + "\n" + "\tLast Name: " + last_name  + "\n" + "\tEmail : " + from_email + "\n" + "\tFeedback : \n\t\t" + msg 
        print(message)
        send_mail('Contact Form',
         message,
         admin_mail,
         ['velvetri452@gmail.com'],
          fail_silently=False)
       
        messages.info(request, f"Mail Sent successfully!..")
        
    return render(request = request,
                  template_name='main/contactus.html',
                  context={})

def accountspage(request):
    return render(request = request,
                  template_name='main/account.html',
                  context={"categories": TutorialCategory.objects.all})

def homepage(request):
    return render(request = request,
                  template_name='main/categories.html',
                  context={"categories": TutorialCategory.objects.all})

def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"New account created: {username}")
            login(request, user)
            messages.info(request, f"You logged in successfully!.. {username}")
            return redirect("main:homepage")

        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")

            return render(request = request,
                          template_name = "main/register.html",
                          context={"form":form})

    form = NewUserForm
    return render(request = request,
                  template_name = "main/register.html",
                  context={"form":form})


def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("main:indexpage")


def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('main:homepage')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request = request,
                    template_name = "main/login.html",
                    context={"form":form})   