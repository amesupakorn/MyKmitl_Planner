from django.shortcuts import redirect
from django.conf import settings

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # ตรวจสอบว่า request นี้เป็นของ authenticated user หรือไม่
        if not request.user.is_authenticated and request.path.startswith('/chat/'):
            return redirect(settings.LOGIN_URL) 

        # ถ้าผู้ใช้ล็อกอินแล้ว ให้ดำเนินการตามปกติ
        response = self.get_response(request)
        return response