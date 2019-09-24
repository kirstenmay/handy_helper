from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt
import datetime


def login_reg(request):
    return render(request, 'login_reg/register.html')

def register(request):
    errors = User.objects.reg_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect('/')
    else:
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        new_user = User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], birthday = request.POST['birthday'], email = request.POST['email'], password = pw_hash)
        request.session['userid'] = new_user.id
        username = new_user.first_name
        request.session['username'] = username
        return redirect("/dashboard")

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect("/")
    else:
        user = User.objects.filter(email = request.POST['login_email'])
        logged_user = user[0]
        request.session['userid'] = logged_user.id
        username = logged_user.first_name
        request.session['username'] = username
        return redirect('/dashboard')

def dashboard(request):
    if 'userid' in request.session:
        context = {
            'other_jobs': Job.objects.exclude(helper = request.session['userid']),
            'user_jobs': Job.objects.filter(helper = request.session['userid'])
        }
        return render(request, 'login_reg/dashboard.html', context)
    else:
        return redirect("/")

def join_job(request, job_id):
    if 'userid' in request.session:
        user = User.objects.get(id = int(request.session['userid']))
        job = Job.objects.get(id = job_id)
        job.helper.add(user)
        return redirect("/dashboard")
    else: 
        return redirect("/")

def leave_job(request, job_id):
    if 'userid' in request.session:
        user = User.objects.get(id = int(request.session['userid']))
        job = Job.objects.get(id = job_id)
        job.helper.remove(user)
        return redirect('/dashboard')
    else:
        return redirect('/')

def edit_job(request, job_id):
    if 'userid' in request.session:
        context = {
            'job': Job.objects.get(id=job_id),
            'all_categories': Category.objects.all()
        }
        return render(request, 'login_reg/edit_job.html', context)
    else: 
        return redirect("/")


def change_job(request):
    if 'userid' in request.session:
        job = Job.objects.get(id = int(request.POST['job']))
        user = Job.objects.get(id = job.id).creator
        if int(request.session['userid']) == user.id:
            errors = Job.objects.edit_job_val(request.POST)
            if len(errors) > 0:
                for key, value in errors.items():
                    messages.error(request, value, extra_tags=key)
                return redirect(f"/edit_job/{job.id}")
            job.title = request.POST['title']
            job.description = request.POST['description']
            job.location = request.POST['location']
            job.save()
            return redirect("/dashboard")
        else:
            return redirect("/dashboard")
    else:
        return redirect("/")

def view_job(request, job_id):
    if 'userid' in request.session:
        job = Job.objects.get(id = job_id)
        context = {
            'current_job': job,
            'categories': job.category.all(),
            'creator': job.creator,
            'helper': job.helper.all(),
        }
        return render(request, 'login_reg/view_job.html', context)
    else: 
        return redirect("/")

def done(request, job_id):
    if 'userid' in request.session:
        job = Job.objects.get(id = job_id)
        job.delete()
        return redirect("/dashboard")
    else: 
        return redirect("/")

def delete(request, job_id):
    if 'userid' in request.session:
        job = Job.objects.get(id = job_id)
        user = Job.objects.get(id = job_id).creator
        if int(request.session['userid']) == user.id:
            job.delete()
            return redirect("/dashboard")
        else: 
            return redirect("/dashboard")
    else: 
        return redirect("/")

def add_job(request):
    if 'userid' in request.session:
        context = {
            'all_categories': Category.objects.all()
        }
        return render(request, 'login_reg/add_job.html', context)
    else: 
        return redirect("/")

def new_job(request):
    if 'userid' in request.session:
        errors = Job.objects.new_job_val(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect("/add_job")
        creator = User.objects.get(id = request.session['userid'])
        job = Job.objects.create(title = request.POST['title'], description = request.POST['description'], location = request.POST['location'], creator = creator)
        if request.POST['new_category']:
            new_category = Category.objects.create(name = request.POST['new_category'])
            new_category.job.add(job)
        else:
            options = request.POST.getlist('category[]')
            for m in options:
                this_category = m
                category = Category.objects.get(id= this_category)
                this_job = Job.objects.get(id=job.id)
                this_job.category.add(category)
        return redirect("/dashboard")
    else:
        return redirect("/")

def log_out(request):
    request.session.clear()
    return redirect("/")