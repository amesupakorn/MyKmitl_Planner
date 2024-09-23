from pyexpat.errors import messages
from django.shortcuts import render,redirect
from django.views import View
from allauth.account.forms import SignupForm, LoginForm
from django.contrib.auth import login  # Import Django's login function


class SignInPage(View):
    
    def get(self, request):
        form = LoginForm()  # ใช้ฟอร์มล็อกอินจาก allauth
        return render(request, "accounts/signin.html", {
            'form': form  # ส่งฟอร์มไปยัง template
        })

    def post(self, request):
        form = LoginForm(request.POST, request=request)  # Pass the request to the form
        if form.is_valid():
            user = form.user  # Retrieve the authenticated user
            login(request, user)  # Use Django's login function to log in the user
            return redirect('planner_dashboard')  # Redirect after successful login
        else:
            # Send the form back with errors
            return render(request, "accounts/signin.html", {
                'form': form
            })


class SignUpPage(View):
    def get(self, request):
        form = SignupForm()
        return render(request, "accounts/signup.html", {'form': form})

    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            try:
                form.save(request)
                return redirect('account_signin')  
            except ValueError as e:
                return render(request, "accounts/signup.html", {'form': form})
        else:
            return render(request, "accounts/signup.html", {'form': form})
