from django.shortcuts import render, redirect
from .models import User, Plan, Activity
from django.contrib import messages
from django.db.models import Count
import bcrypt

# Create your views here.

def index(request):
    # Plan.objects.all().delete()
    return render(request, 'planner/index.html')

# Process for Login and registration
# look at models.py for verification of the different attributes
def process(request):
    # If the button that was pushed is register, it will validate the information
    if request.POST['button'] == 'register':
        register = request.POST
        user = User.objects.register(register)
        # Method returns a tuple and if it is false, it will also return an array containing errors
        if user[0] == False:
            for error in user[1]:
                messages.warning(request, error)
            return redirect('/')
        # If there are no errors, it will return True and the user object
        request.session['id'] = user[1].id
        return redirect('/plan')
    # If the form button pushed was login, it will go through validation for the user
    if request.POST['button'] == 'login':
        user = User.objects.login(request.POST)
        # If the user does not exist or the password does not match the database, errors are returned
        if user[0] == False:
            for error in user[1]:
                messages.warning(request, error)
            return redirect('/')
        # If login was successful, the user object is returned
        else:
            request.session['id'] = user[1].id
            return redirect('/plan')

def plan(request):
    if request.session.get('id') == None:
        return redirect('/')
    context = {
        'user': User.objects.get(id = request.session['id']),
        'plans': Plan.objects.filter(users_id = request.session['id'])
    }
    return render(request, 'planner/planner.html', context)

def newplan(request):
    if request.session.get('id') == None:
        return redirect('/')
    user = User.objects.get(id = request.session['id'])
    Plan.objects.create(city = request.POST['city'], start_location = request.POST['start_location'], users_id = user)
    # Since it is a new plan, the following query will grab the last entry to the database
    plan_id = Plan.objects.order_by('-id')[0]
    return redirect('/activity/' + str(plan_id.id))

def activity(request, plan_id):
    if request.session.get('id') == None:
        return redirect('/')
    request.session['plan_id'] = plan_id
    context = {
        'start': Plan.objects.get(id = plan_id),
    }
    return render(request, 'planner/activity.html', context)

def addActivity(request, plan_id):
    if request.session.get('id') == None:
        return redirect('/')
    plan = Plan.objects.get(id = plan_id)
    Activity.objects.create(activity_type = request.POST['newActivity'], plans_id = plan)
    return redirect('/activity/' + str(plan_id))

def showPlan(request, plan_id):
    if request.session.get('id') == None:
        return redirect('/')
    context = {
        'start': Plan.objects.get(id = plan_id),
        'activities': Activity.objects.filter(plans_id = plan_id)
    }
    return render(request, 'planner/currentPlan.html', context)

def deleteActivity(request, plan_id, activity_id):
    if request.session.get('id') == None:
        return redirect('/')
    Activity.objects.get(id = activity_id).delete()
    return redirect('/activity/' + str(plan_id) + '/show')

def logout(request):
    request.session.pop('id')
    request.session.pop('plan_id')
    return redirect('/')
