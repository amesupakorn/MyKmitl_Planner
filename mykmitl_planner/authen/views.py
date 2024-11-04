from django.contrib import messages
from django.shortcuts import render,redirect
from django.views import View
from allauth.account.forms import SignupForm, LoginForm
from allauth.account.forms import ResetPasswordForm, SetPasswordForm
from django.contrib.auth import login, logout  # Import Django's login function
from planner.models import Student, UniversityStaff
from django.contrib.auth.models import User
from .forms import ProfileForm, ProfileStaff
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.db import transaction
from django.contrib.auth.models import Group

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


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
            
            try:
                with transaction.atomic():
                    if not user.emailaddress_set.filter(verified=True).exists():
                        messages.error(request, "Please verify your email before logging in.")
                        return render(request, "account/signin.html", {'form': form})

                    messages.success(request, "You have signed in successfully.")
                    login(request, user)

                    if user.is_staff:
                        return redirect('staff_dashboard')

                    return redirect('planner_dashboard')

            except Exception as e:
                # ถ้ามีข้อผิดพลาด ให้ rollback transaction
                messages.error(request, "An error occurred. Please try again.")
                return render(request, "account/signin.html", {'form': form})
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
            # ตรวจสอบว่าอีเมลลงท้ายด้วย '@kmitl.ac.th'
            email = form.cleaned_data.get('email')
            if not email.endswith('@kmitl.ac.th'):
                messages.error(request, "You must use a KMITL email address (kmitl.ac.th)")
                return render(request, "account/signup.html", {'form': form})

            try:
                with transaction.atomic():
                    user = form.save(self.request)
                    userid = User.objects.get(username=user.username)
                    
                    # สร้างข้อมูล Student
                    Student.objects.create(
                        student_user=userid,
                        email=user.email
                    )
                    
                    group, created = Group.objects.get_or_create(name='student')
                    user.groups.add(group)
                    
                    email_address = user.emailaddress_set.get(email=user.email) 
                    if not email_address.verified:
                        email_address.send_confirmation(self.request)  # ส่งอีเมลยืนยันอีกครั้งหากยังไม่ได้ยืนยัน
                    
                    messages.success(request, "You have signed up successfully.")
                    return redirect('account_email_confirmation')
            except ValueError as e:
                messages.error(request, f"An error occurred: {str(e)}")

                return render(request, "account/signup.html", {'form': form})
        else:
            messages.error(request, "Please correct the errors below.")

            return render(request, "account/signup.html", {'form': form})

class EmailConfirmationSentView(View):
    
    def get(self, request):
        return render(request, "account/email_confirmemail.html", {})    

class LogOutPage(View):
 
    def get(self, request):
        logout(request)
        messages.success(request, "You have been logged out successfully.")
        return redirect('account_login')
    
class EditProfile(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/auth'
    permission_required = ["planner.change_student", "planner.view_student"]
    
    def get(self, request):
        # ดึงข้อมูลโปรไฟล์ของผู้ใช้ปัจจุบัน
        student = Student.objects.get(student_user=request.user)
        form = ProfileForm(instance=student)
        formpass = PasswordChangeForm(user=request.user)
        
        return render(request, "editaccount.html", {
            'form': form,
            'formpass' : formpass,
            'student': student,  
        })

    def post(self, request):

        student = Student.objects.get(student_user=request.user)
        form = ProfileForm(request.POST, request.FILES, instance=student)

        if form.is_valid():
            form.save()  # บันทึกข้อมูลที่แก้ไข
            messages.success(request, "update profile successfully")
            return redirect('profile')  # เปลี่ยนเส้นทางไปยังหน้าดูโปรไฟล์
        
        return render(request, "editaccount.html", {
            'form': form,
            'student': student,
        })

class EditProfileStaff(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/auth'
    permission_required = ["planner.change_universitystaff"]

    def get(self, request):
        # ดึงข้อมูลโปรไฟล์ของผู้ใช้ปัจจุบัน
        staff = UniversityStaff.objects.get(staff_user=request.user)
        form = ProfileStaff(instance=staff)
        formpass = PasswordChangeForm(user=request.user)
        
        return render(request, "editStaff.html", {
            'form': form,
            'formpass' : formpass,
            'staff': staff,  
        })

    def post(self, request):

        staff = UniversityStaff.objects.get(staff_user=request.user)        
        form = ProfileStaff(request.POST, instance=staff)

        if form.is_valid():
            form.save() 
            messages.success(request, "update profile successfully")
            return redirect('accountstaff')  
        
        return render(request, "editStaff.html", {
            'form': form,
            'staff': staff,
        })

class PasswordChangeView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/auth'
    permission_required = ["planner.change_student"]
    def post(self, request):
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Your password has been changed successfully.")
            return redirect('profile')  # Redirect ไปหน้าโปรไฟล์หรือหน้าอื่นที่ต้องการ
        else:
            messages.error(request, "There was an error with your changed password. Please try again.")
            return render(request, 'account/password_change.html', {
                'form': form
            })

class PasswordForgotView(View):
    form_class = ResetPasswordForm

    def get(self, request):
        form = self.form_class()
        return render(request, 'account/forgot_password.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')

            # ตรวจสอบว่า email มีอยู่ในฐานข้อมูลหรือไม่
            if not User.objects.filter(email=email).exists():
                messages.error(request, "This email address is not associated with any account.")
                return render(request, 'account/forgot_password.html', {'form': form})

            # ถ้ามีอีเมลอยู่ในระบบแล้วให้ทำการส่งคำขอ reset password
            form.save(
                request=request,
                use_https=request.is_secure(),  # ใช้ HTTPS ถ้าเป็น secure request
                email_template_name='account/email/password_reset_key_message.html'  # อีเมล template
            )
            messages.success(request, "Password reset instructions have been sent to your email.")
            return redirect('account_login')

        # ถ้า form ไม่ valid ให้แสดงข้อผิดพลาด
        return render(request, 'account/forgot_password.html', {'form': form})


