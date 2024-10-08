from rest_framework import permissions

class ChatMessagePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS: 
            return request.user.has_perm('chat.view_message')
        elif request.method == 'POST':
            return request.user.has_perm('chat.add_message')
        return False
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return request.user.has_perm("chat.view_message") and obj.staff.staff_user == request.user
        elif request.method == 'POST':
            return request.user.has_perm('chat.add_message')
        return False
