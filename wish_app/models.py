from django.db import models
import re
from django.shortcuts import render, redirect, HttpResponse


# Create your models here.

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]+$")
# email has been set as type='email'. To make sure do one changed throught inspect


class UserManager(models.Manager):
    def user_validation(self, postData):
        errors = {}
        if len(postData['firstName']) < 2:
            errors['firstName'] = 'First Name should be at least 2 characters'
        if len(postData['lastName']) < 2:
            errors['lastName'] = 'Last Name should be at least 2 characters'
        if len(postData['password']) < 8:
            errors['password'] = 'Password should be at least 8 characters'
        if postData['password'] != postData['confirmPassword']:
            errors['confirmPassword'] = 'Passwords doest match'
        if User.objects.filter(email=postData['email']):
            errors['email'] = 'This email already registered'
        if not EMAIL_REGEX.match(postData['email']):
            errors['invalid_email'] = 'Invalid email adress'
        return errors


class WishManager(models.Manager):
    def wish_validator(self, postData):
        errors = {}
        if len(postData['wish']) < 3:
            errors['wish_error'] = 'A wish must consist of at least 3 characters!'
        if len(postData['description']) < 3:
            errors['description_error'] = 'A description must be provided (at least 3 characters)'
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Wish(models.Model):
    item = models.CharField(max_length=255)
    desc = models.CharField(max_length=255)
    user = models.ForeignKey(
        User, related_name='wishes', on_delete=models.CASCADE)
    added_date = models.DateField(auto_now_add=True)
    objects = WishManager()


class Granted(models.Model):
    user = models.ForeignKey(
        User, related_name='granted', on_delete=models.CASCADE)
    item = models.CharField(max_length=255)
    added_date = models.DateField(blank=True)
    granted_date = models.DateField(auto_now_add=True)
    liked = models.ManyToManyField(User, related_name='liked')
