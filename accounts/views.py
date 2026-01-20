import random

from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.shortcuts import redirect, render

from .Email import EmailLogin
from .forms import LoginForm, RegistationForm, UserClient
from .models import User


# Create your views here.


def sign_client(request):
    form = UserClient()
    if request.method == "POST":
        form = UserClient(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = generate(
                form.cleaned_data["first_name"], form.cleaned_data["last_name"]
            )
            new_user.save()
            print(new_user.username)
            return redirect("signin")

    return render(request, "signup.html", {"form": form})


def registration(request):
    if request.method == "POST":
        print("post request in registaion")
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        password1 = request.POST["password"]
        password2 = request.POST["confirm_password"]
        username = generate(first_name, last_name)
        role_value = request.POST.get("role")
        role_map = {
            "artisan": User.Role.HANDYMAN,
            "handyman": User.Role.HANDYMAN,
            "client": User.Role.CUSTOMER,
            "customer": User.Role.CUSTOMER,
            "admin": User.Role.ADMIN,
        }
        role = role_map.get(role_value, User.Role.CUSTOMER)
        errors = []

        if not all([first_name, last_name, email, password1, password2]):
            print("errrrrrrrrrrrrrrrrrrrrrrrrrrrror")
            print(first_name)
            errors.append("Tous les champs sont obligatoires.")

        try:
            validate_email(email)
        except ValidationError:
            print("Format d'email invalide.")
            errors.append("Format d'email invalide.")

        if User.objects.filter(email=email).exists():
            print("Un compte avec cet email existe déjà.")
            errors.append("Un compte avec cet email existe déjà.")

        if password1 != password2:
            print("Les mots de passe ne correspondent pas.")
            errors.append("Les mots de passe ne correspondent pas.")

        if len(password1) < 8:
            print("Le mot de passe doit contenir au moins 8 caractères.")
            errors.append("Le mot de passe doit contenir au moins 8 caractères.")

        if errors:
            print("i am in error")
            for error in errors:
                messages.error(request, error)
            return render(
                request,
                "registration.html",
                {"first_name": first_name, "last_name": last_name, "email": email},
            )

        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1,
                first_name=first_name,
                last_name=last_name,
                role=role,
            )

            return redirect("home_page")

        except Exception:
            messages.error(request, "Une erreur s'est produite lors de l'inscription.")
            return render(request, "registration.html")

    print("hey why")
    return render(request, "registration.html")


# view de signup
def sign_up(request):
    form = RegistationForm()
    if request.method == "POST":
        form = RegistationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = generate(
                form.cleaned_data["first_name"], form.cleaned_data["last_name"]
            )
            new_user.role = User.Role.HANDYMAN
            print(form.cleaned_data["last_name"])
            print(form.cleaned_data["first_name"])
            new_user.save()
            print(new_user.username)
            return redirect("signin")

    return render(request, "join.html", {"form": form})


def generate(first_name, last_name):
    charaters = [
        "!",
        '"',
        "#",
        "$",
        "%",
        "&",
        "'",
        "(",
        ")",
        "*",
        "+",
        ",",
        "-",
        ".",
        "/",
        ":",
        ";",
        "<",
        "=",
        ">",
        "?",
        "@",
        "[",
        "\\",
        "]",
        "^",
        "_",
        "`",
        "{",
        "|",
        "}",
        "~",
        "0",
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
    ]
    username = (
        f"{random.choice(charaters)}{last_name}{random.choice(charaters)}"
        f"{first_name}{random.choice(charaters)}"
    )
    return username


# view de sign in
def sign_in(request):
    if request.user.is_authenticated:
        return redirect("home")
    form = LoginForm()
    if request.method == "POST":
        loginEmail = EmailLogin()
        email = request.POST["email"]
        password = request.POST["password"]
        user = loginEmail.authenticate(request, email, password)

        if user is not None:
            login(request, user)
            return redirect("home")
        return render(request, "signin.html", {"eror": "there is a problem"})
    return render(request, "signin.html", {"form": form})


def home_page(request):
    if request.user.is_authenticated:
        return redirect("services:home")
    form = LoginForm()
    return render(request, "home_page.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("signin")


def sendEmail(request):
    if request.method == "POST":
        email = request.POST["email"]
        send_mail(
            "Subject here",
            "Here is the message.",
            "elmehdiiskandar3@gmail.com",
            [f"{email}"],
            fail_silently=False,
        )
        return render(
            request,
            "email_form.html",
            {"success": "you the email is in your inbox check it"},
        )

    return render(request, "email_form.html")
