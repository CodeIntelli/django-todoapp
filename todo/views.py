from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as loginUser, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import TODOForm

from django.contrib.auth.decorators import login_required
from .models import TODO
# Create your views here.


def home(request):
    if request.user.is_authenticated:
        user = request.user
        form = TODOForm()
        todos = TODO.objects.filter(user=user).order_by('priority')
        return render(request, 'index.html', context={'form': form, 'todos': todos})


def login(request):
    if request.method == 'GET':
        form = AuthenticationForm()
        context = {'form': form}
        return render(request, 'login.html', context)

    else:
        form = AuthenticationForm(data=request.POST)
        context = {'form': form}
        if form.is_valid():
            print('form is valid')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            print('*******user***********', user)
            if user is not None:
                loginUser(request, user)
                return redirect('home')
            return render(request, 'signup.html', context)
        else:
            return render(request, 'login.html', context)


def signup(request):
    if request.method == 'GET':
        form = UserCreationForm()
        context = {
            "form": form,
        }
        return render(request, 'signup.html', context)

    else:
        print(request.POST)
        form = UserCreationForm(request.POST)
        context = {
            "form": form,
        }
        if form.is_valid():
            user = form.save()
            print(user)
            if user is not None:
                return redirect('login')
            return render(request, 'signup.html', context)
        else:
            return render(request, 'signup.html', context)


@login_required(login_url='login')
def add_todo(request):
    if request.user.is_authenticated:
        user = request.user
        print(user)
        form = TODOForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            todo = form.save(commit=False)
            todo.user = user
            todo.save()
            print(todo)
            return redirect("home")
        else:
            return render(request, 'index.html', context={'form': form})


def delete_todo(request, id):
    print(id)
    TODO.objects.get(pk=id).delete()
    return redirect('home')


def change_todo(request, id, status):
    todo = TODO.objects.get(pk=id)
    todo.status = status
    todo.save()
    return redirect('home')


def signout(request):
    logout(request)
    return redirect('login')
