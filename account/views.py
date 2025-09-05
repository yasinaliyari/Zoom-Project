from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET
from django.contrib.auth import login, authenticate, logout

from account.forms import RegisterForm, LoginForm, TeamForm
from account.models import Team


@require_GET
def home(request):
    if request.user.is_authenticated:
        if request.user.team:
            team_name = request.user.team.name
        else:
            team_name = "None"
    else:
        team_name = "None"

    return render(request, "home.html", {"team": team_name})


def signup(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("team")
        else:
            return render(request, "signup.html", {"form": form})
    else:
        form = RegisterForm()
        return render(request, "signup.html", {"form": form})


def login_account(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                form.add_error(None, "The username or password is incorrect.")
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})


@require_GET
def logout_account(request):
    logout(request)
    return redirect("login")


@login_required
def join_or_create_team(request):
    if request.method == "GET":
        if request.user.team:
            return redirect("home")
        form = TeamForm()
        return render(request, "team.html", {"form": form})
    if request.method == "POST":
        form = TeamForm(request.POST)
        if form.is_valid():
            team_name = form.cleaned_data["name"]
            team, created = Team.objects.get_or_create(name=team_name)
            request.user.team = team
            request.user.save()
            return redirect("home")
        else:
            return redirect("home")


@require_GET
def exit_team(request):
    if request.user.team:
        request.user.team = None
        request.user.save()
    return redirect("home")
