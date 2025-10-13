from django.shortcuts import redirect, render
from django.contrib import messages
from .forms import UserForm
from django.conf import settings
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from .utils import send_activation_email
from .models import User
from django.contrib.auth import authenticate, login as auth_login 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm   
from django.contrib.auth import logout
from .forms import passwordResetForm ,  UserForm
from account.utils import send_password_reset_email


def home(request):
    return render(request, 'home.html', )

def register(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.is_active = False
            user.save()

            # Send activation email
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            activation_link = reverse('activate', kwargs={'uidb64': uid, 'token': token})
            activation_url = f"{settings.SITE_URL.rstrip('/')}{activation_link}"
            send_activation_email(user.email, activation_url)

            messages.success(request, "Registration successful please check your email to activate your account.")
            return redirect('register')
        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        form = UserForm()

    return render(request, 'register.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        if user.is_active:
            messages.warning(request, "Account is already activated.")
            return redirect('login')
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, "Account activated successfully. You can now log in.")
            return redirect('login')
        else:
            messages.error(request, "Activation link is invalid or has expired.")
            return redirect('login')
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        messages.error(request, "Invalid activation link.")
        return redirect('login')


def login(request):
    if request.method == "POST":
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

        if not email or not password:
            messages.error(request, "Please provide both email and password.")
            return redirect('login')

        user = authenticate(request, email=email, password=password)
        if user is None:
            # Give a specific message for inactive accounts
            existing = User.objects.filter(email=email).first()
            if existing and not existing.is_active:
                messages.error(request, "Account is not activated. Please check your email.")
            else:
                messages.error(request, "Invalid email or password.")
            return redirect('login')

        auth_login(request, user)  # call Django's login
        return redirect('home')

    return render(request, 'login.html')

@login_required
def password_reset(request):
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Password updated successfully.")
            logout(request)
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
            return render(request, 'password_reset.html', {'form': form})
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'password_reset.html', {'form': form})

def forgot_password(request):
    if request.method == "POST":
        form=passwordResetForm(request.POST)
        if form.is_valid():
            email=form.cleaned_data.get('email')
            user=User.objects.filter(email=email).first()
            if user:
                 #generate token and uid

                 uid = urlsafe_base64_encode(force_bytes(user.pk))
                 token = default_token_generator.make_token(user)

                 #create password reset url
                 reset_url = reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
                 absolute_url=f"{request.build_absolute_uri(reset_url)}"

                 #send password reset email
                 send_password_reset_email(user.email, absolute_url)

                 messages.success(request, "Password reset link has been sent to your email.")
                 return redirect('login')
  
            else:
                messages.error(request, "No user is associated with this email.")
        else:
            # Show form validation errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    else:
        form = passwordResetForm()
    
    return render(request, 'forgot_password.html', {'form': form})


def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == "POST":
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Password has been reset. You can now log in.")
                return redirect('login')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, error)
        else:
            form = SetPasswordForm(user)
        return render(request, 'password_reset_confirm.html', {'form': form ,'uidb64': uidb64, 'token': token})
    else:
        messages.error(request, "The reset link is invalid or has expired.")
        return redirect('forgot_password')