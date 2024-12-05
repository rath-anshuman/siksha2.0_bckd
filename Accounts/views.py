from django.shortcuts import render
from django.http import JsonResponse
from Accounts.models import UserAccount,Verification
from django.contrib.auth import authenticate

from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view

import random
from django.core.mail import send_mail

@api_view(['POST'])
def login(request):
    if request.method=='POST':
        regno = request.data.get('regno')
        pssd = request.data.get('password')
        user = authenticate(regno=regno, password=pssd)
        print(user)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'regno': user.regno})
        return Response({'error': 'Invalid credentials'}, status=400)

@api_view(['POST'])
def send_otp_email(request):
    email=request.data.get('email')
    subject = "Your OTP for Signup to Siksha."
    otp=str(random.randint(100000, 999999))
    try:
        verification = Verification.objects.get(email=email)
        verification.otp = otp
        verification.save()
    except Verification.DoesNotExist:
        verification = Verification.objects.create(email=email, otp=otp)
    message = f'''Use this {otp} register yourself at Siksha. THE OTP IS VALID FOR 5 MINITUES ONLY !'''
    from_email = 'sanskaricoders@gmail.com'
    send_mail(subject, message, from_email, [email])
    return Response({'Succesfull':'Otp send Successfully.'})

@api_view(['POST'])
def signup(request):
    if request.method == 'POST':
        email = request.data.get('email')
        name = request.data.get('name')
        regno = request.data.get('regno')
        section = request.data.get('section')
        password = request.data.get('password')
        otp = request.data.get('otp')

        if UserAccount.objects.filter(regno=regno).exists():
            return Response({'error': 'Registration number already exists'}, status=400)

        if UserAccount.objects.filter(email=email).exists():
            return Response({'error': 'Email already linked with another Registration Number'}, status=400)

        try:
            verification = Verification.objects.get(email=email)

            if not verification.is_valid():
                return Response({'error': 'OTP has expired'}, status=400)

            if verification.otp != otp:
                return Response({'error': 'Invalid OTP'}, status=400)
            
        except Verification.DoesNotExist:
            return Response({'error': 'No OTP sent for this email'}, status=400)

        user = UserAccount.objects.create_user(
            email=email,
            name=name,
            regno=regno,
            section=section,
            password=password,  
        )

        verification.delete()

        return Response({
            'message': 'User registered successfully',
            'regno': user.regno,
            'name': user.name,
        })

