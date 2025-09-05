from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET
from django.contrib.auth import login, authenticate
from account.forms import RegisterForm, LoginForm


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
    pass


def logout_account(request):
    pass


@login_required
def joinoradd_team(request):
    pass


def exit_team(request):
    pass
