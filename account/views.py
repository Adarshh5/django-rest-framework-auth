from django.shortcuts import render,  redirect
from django.views import View
from .forms import RegistertionForm, CustomLoginForm, CustomPasswordChangeForm, PasswordResetForm
from django.contrib import messages
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from account.utils import send_activation_email, send_reset_passsword_email
from account.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import logout
from django.contrib.auth.forms import SetPasswordForm
import os
 

from dotenv import load_dotenv
load_dotenv()
 



def register(request):
    if request.method == 'POST':
       form = RegistertionForm(request.POST)
       if form.is_valid():
           user = form.save(commit=False)
           user.set_password(form.cleaned_data['password'])
           user.is_active = False
           user.save()

           uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
           token = default_token_generator.make_token(user)
           activation_link = reverse('activate', kwargs={'uidb64': uidb64, 'token': token})
           activation_url = f'{settings.SITE_DOMAIN}{activation_link}'
           send_activation_email(user.email, activation_url)



           messages.success(
               request, "Registration Susseful! Please check your email to activate your account. ",
           )


           return redirect('login')
       

    else:
        form = RegistertionForm()
    return render(request, 'account/registration.html', {'form': form})


def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

        if user.is_active:
            messages.warning(request, "This account has already been activated")
            return redirect('login')
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, 'Your account has been activated successfully!')
            return redirect('login')
        else:
            messages.error(request, 'The activation link is invalid or has expired')
            return redirect('login')

    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        messages.error(request, "Invalid activation link.")
        return redirect('login')


def login_view(request):
    if request.method == "GET": 
        form = CustomLoginForm()
        return render(request, 'account/login.html', {'form': form})
  

    if request.method == "POST":
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']  
            password = form.cleaned_data['password']

            if not email or not password:
                messages.error(request, 'Both fields are required.')
                return redirect('login')

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                messages.error(request, "Invalid email or password.")
                return redirect('login')

            if not user.is_active:
                messages.error(request, "Your account is inactive. Please activate your account.")
                return redirect('login')

            user = authenticate(request, email=email, password=password)  
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Invalid email or password.")

    return render(request, 'account/login.html', {'form': form})







def ChangePasswordView(request):
    if request.method == "POST":
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            logout(request)
            messages.success(request, "Password Changed successfully, Please log in with your new password")
            return redirect('login')

        else:
            for field, errors in form.errors.items():
                for error in errors:
                  messages.error(request, error)

    else:
       form = CustomPasswordChangeForm(user=request.user) 
    return render(request, 'account/ChangePassword.html', {'form':form})




def password_reset_view(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            user =  User.objects.filter(email=email).first()
            if user:
                
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                reset_url = reverse('password_reset_confirm', kwargs={'uidb64': uidb64, 'token': token})
                absolute_reset_url = f"{request.build_absolute_uri(reset_url)}"
                print(absolute_reset_url)
                send_reset_passsword_email(user.email, absolute_reset_url)
                messages.success(request, (
                    "We have sent you a password reset link. please check your email"

                ))
                return redirect('login')

    else:
        form = PasswordResetForm()
        return render(request, 'account/password_reset.html', {"form": form})
    


def password_reset_confirm_view(request, uidb64, token):
     try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        if not default_token_generator.check_token(user, token):
           messages.error(request, 'This link has expired or is invalid')
           return redirect('paasword_reset')
        
        if request.method == "POST":
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success( request, ('Your password has been successfuly reset'))
                return redirect('login')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, error)
                        return redirect('password_reset')
                    
        else:
            form = SetPasswordForm(user)
            return render(request, 'account/password_reset_confirm.html', {'form' :form, 'uidb64': uidb64, 'token': token})


     except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        messages.error(request, "An error occurred. Please try again later. ")
        return redirect('password_reset')
     


def endpoint(request):
    return render(request, "account/endpointinfo.html")