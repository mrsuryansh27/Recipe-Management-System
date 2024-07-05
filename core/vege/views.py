from django.shortcuts import render, redirect
from .models import Receipe
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

@login_required(login_url="/login/")
def receipes(request):
    if request.method == "POST":
        data = request.POST
        receipe_image = request.FILES.get('receipe_image')
        receipe_name = data.get('receipe_name')
        receipe_description = data.get('receipe_description')
        
        Receipe.objects.create(
            receipe_image=receipe_image,
            receipe_name=receipe_name,
            receipe_description=receipe_description
        )
        
        return redirect('receipes')
    
    # Handle search functionality
    search_query = request.GET.get('search')
    queryset = Receipe.objects.all()
    if search_query:
        queryset = queryset.filter(receipe_name__icontains=search_query)
    
    context = {'receipes': queryset, 'search_query': search_query}
    return render(request, 'receipes.html', context)

def update_receipe(request, id):
    receipe = Receipe.objects.get(id=id)
    
    if request.method == "POST":
        data = request.POST
        receipe_image = request.FILES.get('receipe_image')
        receipe.receipe_name = data.get('receipe_name')
        receipe.receipe_description = data.get('receipe_description')
        
        if receipe_image:
            receipe.receipe_image = receipe_image

        receipe.save()

        return redirect('receipes')
    
    context = {'receipe': receipe}
    return render(request, 'update_receipes.html', context)

def delete_receipe(request, id):
    receipe = Receipe.objects.get(id=id)
    receipe.delete()
    return redirect('receipes')

def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            user = authenticate(username=username, password=password)
            if user is None:
                messages.error(request, 'Invalid Password')
                return redirect('/login/')
            else:
                login(request, user)
                return redirect('/receipes/')
        else:
            messages.error(request, 'User does not exist')
            return redirect('/login/')

    return render(request, 'login.html')

def logout_page(request):
    logout(request)
    return redirect('/login/')

def register(request):

    if request.method =="POST":
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        username=request.POST.get('username')
        password=request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.info(request, 'Username already exists')
            return redirect('/register/')
        
        user=User.objects.create(
        first_name=first_name,
        last_name=last_name,
        username=username )
        user.set_password(password)
        user.save()
        messages.info(request, 'Account Created Successfully')
        return redirect('/register/')

    return render(request, 'register.html')
