from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from corpora.models import Corpus, Lang
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.core.urlresolvers import reverse
from django.utils import timezone
from corpora import views as corpora_views
from django.contrib.auth.decorators import login_required

def login(request):
    '''user = User.objects.create_user('s8tibasu@stud.uni-saarland.de', 's8tibasu@stud.uni-saarland.de', '123456789')
    user.first_name = 'Tiyash'
    user.last_name = 'Basu'
    user.is_active
    user.set_password('123456789')
    user.save'''
    if request.method != "POST":
        return render(request, 'login.html', {})
    else:
        username = request.POST.get('username', False).lower()
        password = request.POST.get('password', False)
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth_login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            context = {"error" : "The username or password is incorrect."}
            return render(request, 'login.html', context)

def logout(request):
    auth_logout(request)
    context = {"message" : "You have successfully logged out."}
    return render(request, 'login.html', context)

def register(request):
    # temporary fix since we don't want to allow new users to register
    return render(request, 'login.html')
    #return render(request, 'register.html', {})

@login_required
def index(request):
    return render(request, 'index.html')

def new_user(request):
    errors = {}
    
    email = request.POST.get('email', False).lower().strip()
    password1 = request.POST['password1'].strip()
    password2 = request.POST['password2'].strip()
    first_name = request.POST['first_name'].strip()
    last_name = request.POST['last_name'].strip()
    
    # Check that both name fields are filled out
    if len(first_name) < 1:
        errors['first_name'] = "First name is required."
    
    if len(last_name) < 1:
        errors['last_name'] = "Last name is required."
    
    # Check that email is not in use
    if User.objects.filter(username=email).exists():
        errors['email'] = "Email is already in use."
        
    # Check password validity
    if not (password1 == password2):
        errors['password2'] = "Passwords do not match."
    
    if(len(password1) < 7):
        errors['password1'] = "Password must be at least 7 characters long."
        
    if(len(errors) > 0):
        context = {"errors" : errors, "email" : email, "first_name" : first_name, "last_name" : last_name}
        return render(request, 'register.html', context)
    
    # We are using email as username, so leave email blank
    user = User.objects.create_user(email, None, password1)
    user.first_name = first_name
    user.last_name = last_name
    
    user.save()
    context = {"message" : "Registration successful!"}
    
    return render(request, 'login.html', context)
