from __future__ import unicode_literals

from django.db import models
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
import re, bcrypt
from datetime import datetime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASS_REGEX = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*(_|[^\w])).+$')

# Create your models here.
class UserManager(models.Manager):
    def register(self, postData):
        errors = []
        # Handle all the errors from the registration
        # Check if the first name is longer than 2 characters and only contains alphabet characters.
        if not (len(postData['first_name']) > 2 and postData['first_name'].isalpha()):
            errors.append('First name cannot contain any numbers and must be longer than one character')
        # Check if last name is longer than 2 characters and contains only characters
        if not (len(postData['last_name']) > 2 and postData['last_name'].isalpha()):
            errors.append('Last name cannot contain any numbers and must be longer than one character')
        # Check if the password is greater than or equal to 8 characters
        if len(postData['password']) <= 8:
            errors.append('Password must be at least 8 characters long')
            # Make sure there is at least one capital letter and a number in the password field
            if not PASS_REGEX.match(postData['password']):
                errors.append('Password must contain one number and one uppercase letter')
        # Check if the two password fields are a match
        if postData['password'] != postData['confirm_password']:
            errors.append('Password and confirm password must match')
        # The email field must follow specific syntax
        if not EMAIL_REGEX.match(postData['email']):
            errors.append("Invalid Email")
        # Check if the email is already registered
        try:
            User.objects.get(email = postData['email'])
            errors.append('Email is already registered')
        except ObjectDoesNotExist:
            pass
        # If there are no errors, create new User object
        if len(errors) == 0:
            hashed = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
            user = User.objects.create(first_name = postData['first_name'], last_name = postData['last_name'], password = hashed, email = postData['email'])
            return (True, user)
        return (False, errors)
    def login(self, postData):
        errors = []
        # Try to find the user in the database using the inputted email
        try:
            user = User.objects.get(email = postData['email'])
            password = postData['password']
            #If there is a user, make sure the password is matching
            if bcrypt.hashpw(password.encode(), user.password.encode()) == user.password:
                return (True, user)
            errors.append("You entered the wrong password.")
        except ObjectDoesNotExist:
            errors.append("The user does not exist")
        return (False, errors)

class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class Plan(models.Model):
    city = models.CharField(max_length = 255, default = "San Francisco")
    start_time = models.DateTimeField(default = None, null = True, blank = True)
    end_time = models.DateTimeField(default = None, null = True, blank = True)
    start_location = models.CharField(max_length = 255, default = None, null = True, blank = True)
    transportation = models.CharField(max_length = 255, default = None, null = True, blank = True)
    users_id = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

# Model for activity is wrong, just need a name, use activity type for name
class Activity(models.Model):
    activity_type = models.CharField(max_length = 255, default = None, null = True, blank = True)
    address = models.CharField(max_length = 255, default = None, null = True, blank = True)
    category = models.CharField(max_length = 255, default = None, null = True, blank = True)
    price = models.PositiveSmallIntegerField(default = None, null = True, blank = True)
    plans_id = models.ForeignKey(Plan)
