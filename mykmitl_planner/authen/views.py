from django.contrib import messages
from django.shortcuts import render,redirect
from django.views import View
from allauth.account.forms import SignupForm, LoginForm
from django.contrib.auth import login, logout  # Import Django's login function
from planner.models import Student
from django.views.generic import TemplateView
from django.contrib.auth.models import User

class SignInPage(View):
    
    def get(self, request):
        form = LoginForm()  # ใช้ฟอร์มล็อกอินจาก allauth
        return render(request, "account/signin.html", {
            'form': form  # ส่งฟอร์มไปยัง template
        })

    def post(self, request):
        form = LoginForm(request.POST, request=request)  # Pass the request to the form
        if form.is_valid():
            user = form.user  
            
            # ตรวจสอบว่าผู้ใช้ยืนยันอีเมลแล้วหรือไม่
            if not user.emailaddress_set.filter(verified=True).exists():
                # หากผู้ใช้ยังไม่ได้ยืนยันอีเมล
                messages.error(request, "Please verify your email before logging in.")
                return render(request, "account/signin.html", {
                    'form': form
                })

            # หากยืนยันอีเมลแล้ว ให้ล็อกอินผู้ใช้
            login(request, user)  # ใช้ฟังก์ชัน login ของ Django เพื่อทำการล็อกอิน
            return redirect('planner_dashboard')  # Redirect หลังจากล็อกอินสำเร็จ
        else:
            # ฟอร์มไม่ถูกต้อง ส่งกลับพร้อมข้อผิดพลาด
            messages.error(request, "Invalid email or password. Please try again.")
            return render(request, "account/signin.html", {
                'form': form
            })


class SignUpPage(View):
    def get(self, request):
        form = SignupForm()
        return render(request, "account/signup.html", {'form': form})

    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(self.request)# ตรวจสอบว่า email address ถูกสร้างขึ้นหรือไม่
                userid = User.objects.get(username = user)
                
                Student.objects.create(
                    student_user = userid,
                    email = user.email
                )
                
                email_address = user.emailaddress_set.get(email=user.email) 
                if not email_address.verified:
                    email_address.send_confirmation(self.request)  # ส่งอีเมลยืนยันอีกครั้งหากยังไม่ได้ยืนยัน
                    
                return redirect('account_email_confirmation')
            except ValueError as e:
                return render(request, "account/signup.html", {'form': form})
        else:
            return render(request, "account/signup.html", {'form': form})

class EmailConfirmationSentView(TemplateView):
    template_name = "account/email_confirmemail_sent.html"
    

class LogOutPage(View):
    
    def get(self, request):
        logout(request)
        messages.success(request, "You have been logged out successfully.")
        return redirect('account_login')