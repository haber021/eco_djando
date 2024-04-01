from django.shortcuts import render
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.core.mail import EmailMessage
import smtplib
from django.core.mail import send_mail
from django.http import HttpResponse
from django.conf import settings
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import auth
from .utils import token_generator
from django.shortcuts import redirect

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login


from django.contrib.auth.tokens import PasswordResetTokenGenerator

from .utils import validate_email  # Assuming you have a validate_email function in utils

from django.urls import reverse



#fast email messeges

import threading
import asyncio
from django.core.mail import send_mail

class EmailThread(threading.Thread):
    def __init__(self, email_message):
        self.email_message = email_message
        threading.Thread.__init__(self)

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.send_email_async())

    async def send_email_async(self):
        await asyncio.sleep(0)  # Allow event loop to run other tasks
        try:
            self.email_message.send()
        except Exception as e:
            print(f"Error sending email: {e}")

    




class ResetPassword(View):
    def get(self, request):
        return render(request, 'authentication/request-password.html')

    def post(self, request):
        email = request.POST.get('email')

        context = {
            'values': request.POST
        }

        if not validate_email(email):
            messages.error(request, 'Please supply a valid email')
            return render(request, 'authentication/request-password.html', context)

        current_site = get_current_site(request)
        user = User.objects.filter(email=email).first()

        if user:
            email_contents = {
                'user': user,
                'domain': current_site.domain,
                'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': PasswordResetTokenGenerator().make_token(user),
            }

            link = reverse('authentication:reset-user-password', kwargs={'uidb64': email_contents['uidb64'], 'token': email_contents['token']})

            reset_url = 'http://' + current_site.domain + link

            email_subject = 'Reset your password'
            email_body = f'Hi {user.username}, please use this link to verify your password: {reset_url}'
            send_mail(email_subject, email_body, settings.DEFAULT_FROM_EMAIL, [email])


            email_message = EmailMessage(
                email_subject,
                email_body,
                settings.DEFAULT_FROM_EMAIL,
                [email]
            )
            
            EmailThread(email_message).start()


            messages.success(request, 'We have sent you an email to reset your password')
            return render(request, 'authentication/request-password.html')
        else:
            messages.error(request, 'No user found with this email address')
            return render(request, 'authentication/request-password.html', context)


from django.utils.http import urlsafe_base64_decode


class CompletePasswordReset(View):
    def get(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token
        }

        try:
            user_id = str(urlsafe_base64_decode(uidb64), 'utf-8')  # Convert bytes to string
            user = User.objects.get(pk=user_id)

            # Check the validity of the token
            if not PasswordResetTokenGenerator().check_token(user, token):
                messages.info(request, 'Password reset link is invalid. Please request a new one.')
                return redirect('authentication:request-password.html')
        except Exception as e:
            return render(request, 'authentication/request-password.html', context)

        return render(request, 'authentication/reset-user-password.html', context)
    
    def post(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token
        }
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:
            messages.error(request, 'Passwords do not match')
            return render(request, 'authentication/reset-user-password.html', context)
        
        if len(password) < 6:
            messages.error(request, 'Password is too short')
            return render(request, 'authentication/reset-user-password.html', context)

        try:
            user_id = str(urlsafe_base64_decode(uidb64), 'utf-8')  # Convert bytes to string
            user = User.objects.get(pk=user_id)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password has been reset successfully. You can now login with your new password.')
            return redirect('authentication:login')
        except Exception as e:
            messages.error(request, 'Something went wrong. Please try again.')
            return render(request, 'authentication/reset-user-password.html', context)
        
        
        # return render(request, 'authentication/reset-user-password.html',context)    





class EmailValidationView(View):
    def post(self, request):
        data=json.loads(request.body)
        email = data['email']

        if not validate_email(email):
            return JsonResponse({'email_error':'email is ivalid'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error':'email in use chooce another one'}, status=409)
        return JsonResponse({'email_valid': True})



class UsernameValidationView(View):
    def post(self, request):
        data=json.loads(request.body)
        username = data['username']

        if not str(username).isalnum():
            return JsonResponse({'username_error':'username should only contain aphanumeric character'}, status=400)
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error':'sorry uusername is use, chooce another one'}, status=409)

        return JsonResponse({'username_valid': True})




    
class SignupView(View):
    def get(self, request):
        return render(request, 'authentication/signup.html')

class ProfileView(View):
    def get(self, request):
        return render(request, 'authentication/profiles.html')

class RegisterView(View):
    def get(self, request):
        return render(request, 'authentication/registers.html')
    
    def post(self, request):

        messages.success(request,'Success the whatsapp success')
        messages.warning(request,'Success the whatsapp warning')
        messages.info(request,'Success the whatsapp info')
        messages.error(request,'Success the whatsapp error')

        return render(request, 'authentication/registers.html')
    


# email verifacation
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .utils import token_generator  # Add this import

class RegisterView(View):
    def get(self, request):
        return render(request, 'authentication/registers.html')

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        context = {'fieldValues': request.POST}

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(request, 'Password too short')
                    return render(request, 'authentication/registers.html', context)

                connection = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
                connection.starttls()
                connection.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.is_active = False
                user.save()

                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                domain = get_current_site(request).domain
                token = token_generator.make_token(user)  # Using token_generator here
                link = reverse('authentication:activate', kwargs={'uidb64': uidb64, 'token': token})
                activate_url = 'http://' + domain + link
                
                email_subject = 'Activate your account'
                email_body = f'Hi {user.username}, please use this link to verify your account: {activate_url}'
                send_mail(email_subject, email_body, settings.DEFAULT_FROM_EMAIL, [email])

                email_message = EmailMessage(
                    email_subject,
                    email_body,
                    settings.DEFAULT_FROM_EMAIL,
                    [email]
                )
                
                EmailThread(email_message).start()


                messages.success(request, 'Account successfully created. Please check your email to activate your account.')
                return render(request, 'authentication/login.html')

        messages.error(request, 'Username or email already exists')
        return render(request, 'authentication/registers.html', context)
    

#
class VerificationView(View):
    def get(self, request, uidb64, token):
        #active user
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=id)

            if not token_generator.check_token(user, token):
                return redirect('authentication:registers'+'?message='+'User already activited')

            if user.is_active:
                return redirect('authentication:registers')
            user.is_active = True
            user.save()

            messages.success(request,'Account activited successfully')
            return redirect('authentication:login')

        except Exception as e:
            pass
            
        return redirect('authentication:login')

# login form


class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, f'Welcome, {user.username}. You are now logged in.')
                    return redirect('bies:index')
                else:
                    messages.error(request, 'Your account is not active. Please check your email.')
            else:
                messages.error(request, 'Invalid credentials. Please try again.')
        else:
            messages.success(request, 'You have been logged out')

        return render(request, 'authentication/login.html')  


#logout
class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, 'You have been logged out')
        return redirect(reverse('authentication:login'))