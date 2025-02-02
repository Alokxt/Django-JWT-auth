from rest_framework.permissions import BasePermission
from rest_framework import serializers
from .models import *
class IsSchoolAdmin(BasePermission):
    """Allow only users with role 'school' to access school admin pages"""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'school'
    

class IsStudent(BasePermission):
    """Allow only users with role 'school' to access school admin pages"""

    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.role == 'student' or request.user.role == 'parent')
    



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only = True)
    role = serializers.ChoiceField(choices=['school', 'parent', 'student'])

    def validate(self, data):
        user = CustomUser.objects.filter(email=data['email'], role=data['role']).first()
        print(user)

        if user and user.check_password(data['password']):
            return data
        raise serializers.ValidationError("Invalid credentials")