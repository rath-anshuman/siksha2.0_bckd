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
    regno = request.data.get('regno')
    pssd = request.data.get('password')
    otp = request.data.get('otp')
    
    user = authenticate(regno=regno, password=pssd)
    if user is None:
        return Response({'error': 'Invalid credentials'}, status=400)
    
    try:
        verification = Verification.objects.get(user=user)
        if not verification.is_valid():
            return Response({'error': 'OTP has expired'}, status=400)
        if verification.otp != otp:
            return Response({'error': 'Invalid OTP'}, status=400)
    except Verification.DoesNotExist:
        return Response({'error': 'No OTP sent for this user'}, status=400)
    verification.delete()
    token, created = Token.objects.get_or_create(user=user)
    return Response({'token': token.key, 'regno': user.regno})


@api_view(['POST'])
def logout(request):
    try:
        token = Token.objects.get(user=request.user)
        token.delete()
        return Response({'message': 'Successfully logged out'}, status=200)
    except Token.DoesNotExist:
        return Response({'error': 'Invalid request or user not logged in'}, status=400)

@api_view(['POST'])
def send_otp_signup(request):
    email = request.data.get('email')
    otp = str(random.randint(100000, 999999))

    if UserAccount.objects.filter(email=email).exists():
        return Response({'error': 'Email is already linked with an existing account'}, status=400)
        
    verification, created = Verification.objects.get_or_create(email=email)

    verification.otp = otp
    verification.save()

    subject = "Your OTP for Signup"
    from_email = 'siksha.iter@soa.ac.in'
    message = f"Use this OTP {otp} to verify yourself at Siksha. This OTP is valid for 5 minutes only!"

    send_mail(subject, message, from_email, [email])

    return Response({'message': f"OTP sent successfully for signup."})

@api_view(['POST'])
def send_otp_login(request):
    regno = request.data.get('regno')
    if not regno:
        return Response({'error': 'Registration number is required'}, status=400)

    try:
        user = UserAccount.objects.get(regno=regno)
    except UserAccount.DoesNotExist:
        return Response({'error': 'No user exists with this registration number'}, status=400)

    otp = str(random.randint(100000, 999999))

    verification, created = Verification.objects.get_or_create(user=user)
    verification.otp = otp
    verification.save()

    subject = "Your OTP for Login"
    from_email = 'siksha.iter@soa.ac.in'
    message = f"Use this OTP {otp} to log in to Siksha. This OTP is valid for 5 minutes only!"

    send_mail(subject, message, from_email, [user.email])

    return Response({'message': "Login OTP sent successfully."})



@api_view(['POST'])
def signup(request):
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
