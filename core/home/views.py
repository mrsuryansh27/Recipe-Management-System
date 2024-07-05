from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def home(request):
    peoples=[
        {'name' : 'Suryansh' , 'age' : 21},
        {'name' : 'Vedu' , 'age' : 22},
        {'name' : 'Mayank' , 'age' : 23},
        {'name' : 'Karan' , 'age' : 24},
        {'name' : 'Sanajay' , 'age' : 25}
    ]
    return render(request, "index.html", context = {'peoples':peoples})
    


def success_page(request):
    return HttpResponse("This is working!")

def about(request):
    context ={'page':'About'}
    return render(request, "about.html",context)

def contact(request):
    context ={'page':'Contact'}
    return render(request, "contact.html",context)
