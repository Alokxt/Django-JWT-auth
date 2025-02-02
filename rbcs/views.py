from django.shortcuts import render
from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .permissions import *
from .models import CustomUser
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework import status
from django.contrib.auth import authenticate
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
# Create your views here.


@api_view(['POST'])
def login_view(request):
   
    s = LoginSerializer(data = request.data)
    
    if s.is_valid():
        email = s.validated_data['email']
        password = s.validated_data['password']
        role = s.validated_data['role']

        user = authenticate(email=email, password=password)

        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            
            url = ''
            if user.role == 'student':
                url = '/student/dashboard/'
            elif(user.role == 'school'):
                url = '/school/dashboard/'
            elif(user.role == 'parent'):
                url = '/parent/dashboard/'

           
            data_response ={
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
                'role':user.role,
                'user_id':user.id,
                'reidrect_url':url
                
            }

          
           
            return Response(data_response)
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsSchoolAdmin])
def school_dashboard(request):
    user = request.user
    sch = CustomUser.objects.filter(email = user.email,role='school').first()
    school = Schools.objects.filter(user = sch).first()
    std = students.objects.filter(school = school)
    l=[]
    for a in std:
        l.append(a.name)
    contex = {'admin':'/admin/'}
    return Response({
        'school': school.name,
        'email': user.email,
        'edit_student_details':'/admin/',
        'students':l
    })
   
   
   



@api_view(['GET'])
@permission_classes([IsStudent])
def student_dash(request):

    user = request.user
    if(user.role!= 'student'):
        return Response({'detail': 'You do not have permission to view this page.'}, status=403)
    
    st = CustomUser.objects.filter(email=user.email, role='student').first()
   
    return Response({
        'id': st.id,
        'email': st.email,
        'role': st.role,
        'name': st.name,
        'Achievements':'/student/achievements/<int:student_id>/'
    })


@api_view(['GET'])
@permission_classes([IsStudent])
def student_acheivemnets(request,student_id):
    st = CustomUser.objects.get(id=student_id)
    cs = students.objects.filter(user = st).first()
    ach = Achievements.objects.filter(student = cs)
    l = []
    for a in ach:
        l.append(a.description)

    return Response({
        'name':st.name,
        'email': st.email,
        'Achievements':l
        
    })


def get_to_login(request):
    return render(request,'login.html')

@api_view(['GET'])
@permission_classes([IsStudent])
def parent_dash(request):
    user = request.user
    p = CustomUser.objects.filter(email = user.email,role='parent').first()
    paret = parent.objects.filter(user = p).first()
    kid = paret.child
    url = 'student/achievements/<int:student_id>/'
    
    
    
    return Response({
        'name':paret.name,
        'email': user.email,
        'student_id':kid.id,
        'student_acheivemnets':url
    })

    

@api_view(['POST'])
def reset_password(request):
    
    email = request.data.get('email')
    my_user = CustomUser.objects.filter(email = email).first()

    uid = urlsafe_base64_encode(force_bytes(my_user.pk))
    token = default_token_generator.make_token(my_user)
    reset_url = f"http://localhost:3000/reset-password/{uid}/{token}/"

    print(token)
    print(uid)
    send_mail(
        'Password Reset Request',
        f'Click the link to reset your password: {reset_url}',
        'alokmanawat6@gmail.com',
        [email],
        fail_silently=False,
    )

    return Response({
        "message": "Password reset link sent!",
        
    } , status=status.HTTP_200_OK)

@api_view(['POST'])
def fortgot(request,token,uidb64):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser.objects.get(pk=uid)

        if not default_token_generator.check_token(user, token):
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
        
        new_password = request.data.get('new_password')
        user.set_password(new_password)
        user.save()

        return Response({"message": "Password has been reset!"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)