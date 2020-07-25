from django.shortcuts import render, redirect, HttpResponse
import bcrypt
from wish_app.models import *
from django.contrib import messages


def index(request):
    return render(request, 'index.html')


def registration(request):
    errors = User.objects.user_validation(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        hash_pwd = bcrypt.hashpw(
            request.POST['password'].encode(), bcrypt.gensalt()).decode()
        new_user = User.objects.create(
            first_name=request.POST['firstName'],
            last_name=request.POST['lastName'],
            email=request.POST['email'],
            password=hash_pwd
        )
        request.session['uid'] = new_user.id
        request.session['user_name'] = new_user.first_name
    return redirect('/wishes')


def user_profile(request):
    context = {
        'user_profile': User.objects.get(id=request.session['uid']),
        'granted_wishes': Granted.objects.all()
    }
    return render(request, 'wishes.html', context)


def login(request):
    errors = {'invalid_credential': 'Email or Password is incorrect'}

    if User.objects.filter(email=request.POST['login_email']).first() == None:
        messages.error(request, errors['invalid_credential'])
        return redirect('/')
    if User.objects.filter(email=request.POST['login_email']).first() != None:
        user = User.objects.filter(email=request.POST['login_email']).first()
        check_pwd = bcrypt.checkpw(
            request.POST['login_password'].encode(), user.password.encode())
        if check_pwd:
            request.session['uid'] = user.id
            request.session['user_name'] = user.first_name
            return redirect('/wishes')
        else:
            messages.error(request, errors['invalid_credential'])

    return redirect('/')


def logout(request):
    del request.session['uid']
    return redirect('/')


def makeAwish(request):
    return render(request, 'new_wish.html')


def submit_wish(request):
    errors = Wish.objects.wish_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/wishes/new')
    else: 
        Wish.objects.create(
            item=request.POST['wish'],
            desc=request.POST['description'],
            user=User.objects.get(id=request.session['uid'])
    )
    return redirect('/wishes')


def remove_wish(request, wish_id):
    Wish.objects.get(id=wish_id).delete()
    return redirect('/wishes')


def edit_wish(request, wish_id):
    context = {
        'edit_wish': Wish.objects.get(id=wish_id)
    }
    return render(request, 'edit_wish.html', context)


def edited_wish(request, wish_id):
    errors = Wish.objects.wish_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/wishes/edit/{wish_id}')
    else: 
        wish = Wish.objects.get(id=wish_id)
        wish.item = request.POST['wish']
        wish.desc = request.POST['description']
        wish.save()
    return redirect('/wishes')


def granted_wish(request, wish_id):
    user = User.objects.get(id=request.session['uid'])
    wish = Wish.objects.get(id=wish_id)
    print(wish.added_date)
    Granted.objects.create(
        user=user,
        item=wish.item,
        added_date=wish.added_date
    )
    Wish.objects.get(id=wish_id).delete()
    return redirect('/wishes')

def stats(request):
    granted_total = Granted.objects.all()
    granted_total = len(granted_total)
    user_granted = User.objects.get(id=request.session['uid']).granted.all()
    user_granted = len(user_granted)
    user_pending = User.objects.get(id=request.session['uid']).wishes.all()
    user_pending = len(user_pending)
    context = {
        'granted_total' : granted_total,
        'user_granted' : user_granted,
        'user_pending' : user_pending
    }
    return render(request, 'stats.html', context)


def liked(request, grant_id):
    user = User.objects.get(id=request.session['uid'])
    grant = Granted.objects.get(id=grant_id)
    grant.liked.add(user)
    
    return redirect('/wishes')


