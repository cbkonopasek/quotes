from __future__ import unicode_literals

from django.db import models
import re
import bcrypt
from datetime import datetime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.

class UserManager(models.Manager):
    def reg_validator(self, postData):
        errors = []
        
        empty = False
        for data in postData:
            if len(postData[data]) is 0:
                empty = True
        if empty:
            errors += ["Please fill out all fields"]
        if len(postData["name"]) < 2:
            errors += ["Name must be at least 2 characters"]
        if len(postData["alias"]) < 2:
            errors += ["Alias must be at least 2 characters"]
        if not EMAIL_REGEX.match(postData["email"]):
            errors += ["That is not a valid email"]

        for user in User.objects.all():
            if postData['email'] == user.email:
                errors += ["That email has already been registred"]
                break
        if len(postData["password"]) < 8:
            errors += ["Password must be at least 8 characters"]
        if postData["password"] != postData["confirm"]:
            errors += ["Passwords did not match"]
        if len(postData['birthday']) != 0:
            if datetime.strptime(postData['birthday'], '%Y-%m-%d') > datetime.now():
                errors += ["You can not be born in the future"]

        return errors

    def login_validator(self, postData):
        errors = []

        if not EMAIL_REGEX.match(postData["email"]):
            errors += ["That is not a valid email"]
            return errors

        isEmail = False
        for user in User.objects.all():
            if user.email == postData['email']:
                isEmail = True
                break
        if not isEmail:
            errors += ["That email has not been registered"]
            return errors

        user = User.objects.get(email = postData['email'])
        if not bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
            errors += ["The password is incorrect for that email"]
            return errors

        return errors

class QuoteManager(models.Manager):
    def quote_validator(self, postData):
        errors = []
        
        empty = False
        for data in postData:
            if len(postData[data]) is 0:
                empty = True
        if empty:
            errors += ["Please fill out all fields"]
        if len(postData["author"]) < 3:
            errors += ["Quoted by must be at least 3 characters"]
        if len(postData["quote"]) < 10:
            errors += ["Message must be at least 10 characters"]

        return errors


class User(models.Model):
    name = models.CharField(max_length = 255)
    alias = models.CharField(max_length = 45)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    birthday = models.DateTimeField(default=datetime.now())
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __repr__(self):
        return "<User Object - id:{}, name: {}>".format(self.id, self.name)

    objects = UserManager()

class Quote(models.Model):
    quote = models.TextField()
    author = models.CharField(max_length = 255)
    posted_by = models.ForeignKey(User, related_name="posted_quotes")
    liked_by = models.ManyToManyField(User, related_name="liked_quotes")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __repr__(self):
        return "<Quote Object - id:{}>".format(self.id)

    objects = QuoteManager()