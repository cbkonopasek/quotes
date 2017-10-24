from django.shortcuts import render, redirect
from django.contrib import messages
from models import *
import bcrypt
from datetime import datetime


# Create your views here.



def index(request):

    return render(request, 'quotes/index.html')

def quotes(request):

    if not request.session['id']:
        return redirect('/')



    context = {
        "alias": User.objects.get(id=request.session['id']).alias,
        "quotes": Quote.objects.exclude(liked_by=User.objects.get(id=request.session['id'])),
        "favs": Quote.objects.filter(liked_by=User.objects.get(id=request.session['id']))
    }

    return render(request, 'quotes/quotes.html', context)

def user(request, num):

    if not request.session['id']:
        return redirect('/')

    context = {
        "quotes": User.objects.get(id=num).posted_quotes.all(),
        "user" : User.objects.get(id=num),
        "count": User.objects.get(id=num).posted_quotes.count(),
    }

    return render(request, 'quotes/user.html', context)





def register(request):
    if request.method == 'POST':
        errors = User.objects.reg_validator(request.POST)
        if len(errors):
            for error in errors:
                messages.error(request, error, extra_tags='reg')
            return redirect('/')
        else:
            passw = request.POST['password']
            hpass = bcrypt.hashpw(passw.encode(), bcrypt.gensalt())
            User.objects.create(name=request.POST["name"], alias=request.POST['alias'], email=request.POST['email'], password=hpass, birthday=request.POST['birthday'])
            request.session['id'] = User.objects.last().id
            return redirect('/quotes')

    else:
         return redirect('/')

def login(request):
    if request.method == 'POST':
        errors = User.objects.login_validator(request.POST)
        if len(errors):
            for error in errors:
                messages.error(request, error, extra_tags ='login')
            return redirect('/')
        else:
            request.session['id'] = User.objects.get(email=request.POST['email']).id
            return redirect('/quotes')

    else:
         return redirect('/')

def add_quote(request):
    if request.method == 'POST':
        errors = Quote.objects.quote_validator(request.POST) 
        if len(errors):
            for error in errors:
                messages.error(request, error)
            return redirect('/quotes')
        else:
            Quote.objects.create(author=request.POST["author"], quote=request.POST['quote'], posted_by=User.objects.get(id=request.session['id']))
            return redirect('/quotes')
    else:
         return redirect('/quotes')

def logout(request):
    del request.session['id']
    return redirect('/')

def like(request):
    if request.method == 'POST':
        quote = Quote.objects.get(id=request.POST['quote_id'])
        User.objects.get(id=request.session['id']).liked_quotes.add(quote)
    return redirect('/quotes')
    
def unlike(request):
    if request.method == 'POST':
        quote = Quote.objects.get(id=request.POST['quote_id'])
        User.objects.get(id=request.session['id']).liked_quotes.remove(quote)
    return redirect('/quotes')