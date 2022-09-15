from re import template
from django.http import HttpResponseRedirect
from django.shortcuts import render
from sys import api_version
import requests
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from urllib import response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics ,permissions
from django.shortcuts import redirect
from knox.models import AuthToken
from sqlalchemy import union
from users.models import TempData, User
from users.serializers import TempDataSerializer,UserSerializer,RegisterSerializer
from users.utils import send_phone_otp,send_email_otp
from users.views import SignUpAPI
from django.contrib.auth import get_user_model ,login

# Create your views here.
class ChangePassword(APIView):
    def patch(self,request):
        user_id = request.data.get('user_id')
        oldpass = request.data.get('oldpass')
        newpass = request.data.get('newpass')
        confirmpass = request.data.get('confirmpass')
        if user_id and oldpass and newpass and confirmpass:
            user = User.objects.filter(Q(id = user_id) & Q(is_del = False)).first()
            if user:
                if newpass == confirmpass:
                    check = user.check_password(oldpass)
                    if check:
                        newencryptpass = make_password(newpass)
                        user.password = newencryptpass
                        user.save()
                        return Response({'message ':'password changed successfully',
                            'status':status.HTTP_200_OK,'success': True })
                    else:
                        return Response({'message ':'username or password is invalid',
                            'status':status.HTTP_400_BAD_REQUEST,'success': False })
                else:
                    return Response({'message ':'newpass and confirmpass must be same',
                            'status':status.HTTP_400_BAD_REQUEST,'success': False })
            else:
                return Response({'message ':'user not found,please enter valid user_id',
                            'status':status.HTTP_400_BAD_REQUEST,'success': False })
        else:
            if user_id is None:
                return Response({'message ':'user_id is Required',
                            'status':status.HTTP_400_BAD_REQUEST,'success': False })
            if oldpass is None:
                return Response({'message ':'oldpass is Required',
                            'status':status.HTTP_400_BAD_REQUEST,'success': False })
            if newpass is None:
                return Response({'message ':'newpass is Required',
                            'status':status.HTTP_400_BAD_REQUEST,'success': False })
            if confirmpass is None:
                return Response({'message ':'confirmpass is Required',
                            'status':status.HTTP_400_BAD_REQUEST,'success': False })

class TempDataAPIView(APIView):
    def get(self, request):
        temp_data = TempData.objects.all()
        serializer = TempDataSerializer(temp_data, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TempDataSerializer(data=request.data)
        phone=request.data.get('phone')
        if phone=='phone':
            phone_number = request.data.get('phone')
            if phone_number:
                phone = str(phone_number)
                temp = TempData.objects.filter(phone=phone).first()   # iexact is case insensitive
                user = User.objects.filter(phone=phone).first()
                print(user)    # iexact is case insensitive for user model
                print(phone)
                if user:
                    return Response({
                        'message': 'User with this Phone number already exists',
                        'status': status.HTTP_400_BAD_REQUEST,
                        'success': False
                    })
            else:
                if serializer.is_valid():
                    serializer.save()
                    dic = serializer.data
                    response = [dic]
                    return Response({
                    'message': 'Temp user created successfully',
                    'status': status.HTTP_200_OK,
                    'success': True,
                    "response": response,
                })
        else:
            return Response({'message ':'Phone and Email Field is Required',
                            'status':'status.HTTP_400_BAD_REQUEST','success': False })


class GetOTP(APIView):
    def post(self, request, *agrs, **kwargs):
        section=request.data.get('section')
        if section=='registration':
            phone_or_email=request.data.get('phone_or_email')
            if phone_or_email=='phone':
                try:
                    phone_number = request.data.get('phone')
                    if phone_number:
                        phone = str(phone_number)
                        temp = TempData.objects.filter(phone=phone).first()   # iexact is case insensitive
                        user = User.objects.filter(phone=phone).first()
                        if user or temp:
                            return Response({
                                'message': 'User with this Phone number already exists',
                                'status': status.HTTP_400_BAD_REQUEST,
                                'success': False
                            })
                        else:
                                te = TempData(phone = phone, section=section,phone_or_email="phone")
                                te.save()
                                data = te
                                old_phone_otp = data.phone_otp
                                new_phone_otp = send_phone_otp(phone)
                                if old_phone_otp:
                                    data.phone_otp = new_phone_otp
                                    data.save()
                                    return Response({
                                        'message': 'Phone OTP sent successfully',
                                        'status': status.HTTP_200_OK,
                                        'success': True,
                                    })
                                else:
                                    data.phone_otp = new_phone_otp
                                    data.save()
                                    return Response({
                                        'message': 'Phone OTP sent successfully',
                                        'status': status.HTTP_200_OK,
                                    })


                    else:
                        return Response({
                            'message': 'Phone number is required',
                            'status': status.HTTP_400_BAD_REQUEST,
                            'success': False,
                        })

                except Exception as e:
                    return Response({
                        'message': str(e),
                        'status': status.HTTP_400_BAD_REQUEST,
                        'success': False,
                    })

            elif phone_or_email=='email':
                try:
                    email = request.data.get('email')
                    if email:
                        temp = TempData.objects.filter(email=email).first()
                        user = User.objects.filter(email=email).first()      # iexact is case insensitive for user model
                        if user or temp:
                            return Response({
                                'message': 'User with this Email already exists',
                                'status': status.HTTP_400_BAD_REQUEST,
                                'success': False
                            })
                        else:
                                te = TempData(email=email,section=section,phone_or_email="email")
                                te.save()
                                data = te
                                old_email_otp = data.email_otp
                                new_email_otp = send_email_otp(email)
                                if old_email_otp:
                                    data.email_otp = new_email_otp
                                    data.save()
                                    return Response({
                                        'message': 'Email OTP sent successfully',
                                        'status': status.HTTP_200_OK,
                                        'success': True,
                                    })
                                else:
                                    data.email_otp = new_email_otp
                                    data.save()
                                    return Response({
                                        'message': 'Email OTP sent successfully',
                                        'status': status.HTTP_200_OK,
                                        'success': True,
                                    })
                    else:
                        return Response({
                            'message': 'Email is required',
                            'status': status.HTTP_400_BAD_REQUEST,
                            'success': False,
                        })
                except Exception as e:
                    return Response({
                        'message': str(e),
                        'status': status.HTTP_400_BAD_REQUEST,
                        'success': False,
                    })
            else:
                return Response({
                        'message': 'please select phone or email',
                        'status': status.HTTP_400_BAD_REQUEST,
                        'success': False,
                    })

        elif section=='edit_profile':
            phone_or_email=request.data.get('phone_or_email')
            user_id = request.data.get('user_id')
            if user_id:
                if phone_or_email=='phone':
                    try:
                        phone_number = request.data.get('phone')
                        if phone_number:
                            phone = str(phone_number)
                            temp = TempData.objects.filter(phone=phone).first()   # iexact is case insensitive
                            user = User.objects.filter(phone=phone).first()      # iexact is case insensitive for user model
                            if user or temp:
                                return Response({
                                    'message': 'User with this Phone number already exists',
                                    'status': status.HTTP_400_BAD_REQUEST,
                                    'success': False
                                })
                            else:
                                    te = TempData(phone=phone,section=section)
                                    te.save()
                                    data = te
                                    old_phone_otp = data.phone_otp
                                    new_phone_otp = send_phone_otp(phone)
                                    if old_phone_otp:
                                        data.phone_otp = new_phone_otp
                                        data.save()
                                        return Response({
                                            'message': 'Phone OTP sent successfully',
                                            'status': status.HTTP_200_OK,
                                            'success': True,
                                        })
                                    else:
                                        data.phone_otp = new_phone_otp
                                        data.save()
                                        return Response({
                                            'message': 'Phone OTP sent successfully',
                                            'status': status.HTTP_200_OK,
                                        })


                        else:
                            return Response({
                                'message': 'Phone number is required',
                                'status': status.HTTP_400_BAD_REQUEST,
                                'success': False,
                            })

                    except Exception as e:
                        return Response({
                            'message': str(e),
                            'status': status.HTTP_400_BAD_REQUEST,
                            'success': False,
                        })

                elif phone_or_email=='email':
                    try:
                        email = request.data.get('email')
                        if email:
                            temp = TempData.objects.filter(email=email).first()
                            user = User.objects.filter(email=email).first()      # iexact is case insensitive for user model
                            if user or temp:
                                return Response({
                                    'message': 'User with this Email already exists',
                                    'status': status.HTTP_400_BAD_REQUEST,
                                    'success': False
                                })
                            else:
                                    te = TempData(email=email,section=section)
                                    te.save()
                                    data = te
                                    old_email_otp = data.email_otp
                                    new_email_otp = send_email_otp(email)
                                    if old_email_otp:
                                        data.email_otp = new_email_otp
                                        data.save()
                                        return Response({
                                            'message': 'Email OTP sent successfully',
                                            'status': status.HTTP_200_OK,
                                            'success': True,
                                        })
                                    else:
                                        data.email_otp = new_email_otp
                                        data.save()
                                        return Response({
                                            'message': 'Email OTP sent successfully',
                                            'status': status.HTTP_200_OK,
                                            'success': True,
                                        })

                        else:
                            return Response({
                                'message': 'Email is required',
                                'status': status.HTTP_400_BAD_REQUEST,
                                'success': False,
                            })
                    except Exception as e:
                        return Response({
                            'message': str(e),
                            'status': status.HTTP_400_BAD_REQUEST,
                            'success': False,
                        })
                else:
                    return Response({
                            'message': 'please select phone or email',
                            'status': status.HTTP_400_BAD_REQUEST,
                            'success': False,
                        })
            else:
                return Response({
                            'message': 'user_id is required',
                            'status': status.HTTP_400_BAD_REQUEST,
                            'success': False,
                        })
        elif section=='login':
            phone_or_email=request.data.get('phone_or_email')
            if phone_or_email=='phone':
                try:
                    phone_number = request.data.get('phone')
                    if phone_number:
                        phone = str(phone_number)   # iexact is case insensitive
                        user = User.objects.filter(phone=phone).first()    # iexact is case insensitive for user model
                        if user:
                            if user.is_verified == False:
                                return Response({
                                'message': 'Please Verify You Account',
                                'status': status.HTTP_404_NOT_FOUND,
                                'success': False,
                            })
                            elif user.is_blocked == True:
                                return Response({
                                'message': 'Your Account is Blocked',
                                'status': status.HTTP_404_NOT_FOUND,
                                'success': False,
                            })
                            else:
                                data = user
                                old_phone_otp = data.phone_otp
                                new_phone_otp = send_phone_otp(phone)
                                if old_phone_otp:
                                    data.phone_otp = new_phone_otp
                                    data.save()
                                    return Response({
                                        'message': 'Phone OTP sent successfully For Login',
                                        'status': status.HTTP_200_OK,
                                        'success': True,
                                    })
                                else:
                                    data.phone_otp = new_phone_otp
                                    data.save()
                                    return Response({
                                        'message': 'Phone OTP sent successfully For Login',
                                        'status': status.HTTP_200_OK,
                                        'success': True,
                                    })
                        else:
                            return Response({
                                'message': 'User with this Phone number is not found',
                                'status': status.HTTP_404_NOT_FOUND,
                                'success': False,
                            })
                    else:
                        return Response({
                            'message': 'Phone number is required',
                            'status': status.HTTP_400_BAD_REQUEST,
                            'success': False,
                        })

                except Exception as e:
                    return Response({
                        'message': str(e),
                        'status': status.HTTP_400_BAD_REQUEST,
                        'success': False,
                    })

            elif phone_or_email=='email':
                try:
                    email = request.data.get('email')
                    if email:
                        user = User.objects.filter(email=email).first()      # iexact is case insensitive for user model
                        if user:
                            data = user
                            old_email_otp = data.email_otp
                            new_email_otp = send_email_otp(email)
                            if old_email_otp:
                                data.email_otp = new_email_otp
                                data.save()
                                return Response({
                                    'message': 'Email OTP sent successfully',
                                    'status': status.HTTP_200_OK,
                                    'success': True,
                                })
                            else:
                                data.email_otp = new_email_otp
                                data.save()
                                return Response({
                                    'message': 'Email OTP sent successfully',
                                    'status': status.HTTP_200_OK,
                                    'success': True,
                                })
                        else:
                            return Response({
                                'message': 'Email-id is not found',
                                'status': status.HTTP_404_NOT_FOUND,
                                'success': False,
                            })
                    else:
                        return Response({
                            'message': 'Email is required',
                            'status': status.HTTP_400_BAD_REQUEST,
                            'success': False,
                        })
                except Exception as e:
                    return Response({
                        'message': str(e),
                        'status': status.HTTP_400_BAD_REQUEST,
                        'success': False,
                    })
            else:
                return Response({
                        'message': 'please select phone or email',
                        'status': status.HTTP_400_BAD_REQUEST,
                        'success': False,
                    })
        else:
            return Response({
                        'message': 'please select section for registration edit_profile or login`',
                        'status': status.HTTP_400_BAD_REQUEST,
                        'success': False,
                    })




class VerifyOTP(APIView):
    def post(self, request, *agrs, **kwargs):
        if request.data.get('section') == 'registration':

            phone_or_email=request.data.get('phone_or_email')
            if phone_or_email=="phone":
                try:
                    phone_number = request.data.get('phone')
                    otp = request.data.get('otp')
                    if phone_number and otp:
                        phone = str(phone_number)
                        temp = TempData.objects.filter(phone=phone).first()
                        if temp:
                            data = temp
                            if data.phone_otp == otp:
                                data.phone_verified = True
                                data.save()
                                return Response({
                                    'message': 'Phone OTP verified successfully',
                                    'status': status.HTTP_200_OK,
                                    'success': True,
                                })

                            else:
                                return Response({
                                    'message': 'Phone OTP is incorrect',
                                    'status': status.HTTP_400_BAD_REQUEST,
                                    'success': False,
                                })
                        else:
                            return Response({
                                'message': 'Phone number not found',
                                'status': status.HTTP_404_NOT_FOUND,
                                'success': False,
                            }
                            )

                    else:
                        return Response({
                            'message': 'Phone number and OTP is required',
                            'status': status.HTTP_400_BAD_REQUEST,
                            'success': False,
                        })
                except Exception as e:
                    return Response({
                        'message': str(e),
                        'status': status.HTTP_400_BAD_REQUEST,
                        'success': False,
                    })
            elif phone_or_email=="email":
                try:
                    email = request.data.get('email')
                    otp = request.data.get('otp')

                    if email and otp:
                        user = TempData.objects.filter(email__iexact=email)
                        if user.exists():
                            data = user.first()
                            if data.email_otp == otp:
                                data.email_verified = True
                                data.save()
                                return Response({
                                    'message': 'email OTP verified successfully',
                                    'status': status.HTTP_200_OK,
                                    'success': True
                                })
                            else:
                                return Response({
                                    'message': 'Email OTP is incorrect',
                                    'status': status.HTTP_400_BAD_REQUEST,
                                    'success': False,
                                })
                        else:
                            return Response({
                                'message': 'Email-id is not found',
                                'status': status.HTTP_404_NOT_FOUND,
                                'success': False,
                            })
                    else:
                        return Response({
                            'message': 'Email and OTP is required',
                            'status': status.HTTP_400_BAD_REQUEST,
                            'success': False,
                        })
                except Exception as e:
                    return Response({
                        'message': str(e),
                        'status': status.HTTP_400_BAD_REQUEST,
                        'success': False,
                    })
            else:
                return Response({
                        'message': 'please select phone or email',
                        'status': status.HTTP_400_BAD_REQUEST,
                        'success': False,
                    })

        elif request.data.get('section') == 'edit_profile':

            phone_or_email=request.data.get('phone_or_email')
            user_id = request.data.get('user_id')
            if user_id:
                if phone_or_email=="phone":
                    try:
                        phone_number = request.data.get('phone')
                        otp = request.data.get('otp')
                        if phone_number and otp:
                            phone = str(phone_number)
                            temp = TempData.objects.filter(phone=phone).first()
                            if temp:
                                data = temp
                                if data.phone_otp == otp:
                                    data.phone_verified = True
                                    data.save()
                                    return Response({
                                    'message': 'Phone OTP verified successfully',
                                    'status': status.HTTP_200_OK,
                                    'success': True,
                                })


                                else:
                                    return Response({
                                        'message': 'Phone OTP is incorrect',
                                        'status': status.HTTP_400_BAD_REQUEST,
                                        'success': False,
                                    })
                            else:
                                return Response({
                                    'message': 'Phone number not found',
                                    'status': status.HTTP_404_NOT_FOUND,
                                    'success': False,
                                }
                                )

                        else:
                            return Response({
                                'message': 'Phone number and OTP is required',
                                'status': status.HTTP_400_BAD_REQUEST,
                                'success': False,
                            })
                    except Exception as e:
                        return Response({
                            'message': str(e),
                            'status': status.HTTP_400_BAD_REQUEST,
                            'success': False,
                        })
                elif phone_or_email=="email":
                    try:
                        email = request.data.get('email')
                        otp = request.data.get('otp')

                        if email and otp:
                            user = TempData.objects.filter(email__iexact=email)
                            if user.exists():
                                data = user.first()
                                if data.email_otp == otp:
                                    data.email_verified = True
                                    data.save()
                                    return Response({
                                    'message': 'email OTP verified successfully',
                                        'status': status.HTTP_200_OK,
                                        'success': True
                                        })
                                else:
                                    return Response({
                                        'message': 'Email OTP is incorrect',
                                        'status': status.HTTP_400_BAD_REQUEST,
                                        'success': False,
                                    })
                            else:
                                return Response({
                                    'message': 'Email-id is not found',
                                    'status': status.HTTP_404_NOT_FOUND,
                                    'success': False,
                                })
                        else:
                            return Response({
                                'message': 'Email and OTP is required',
                                'status': status.HTTP_400_BAD_REQUEST,
                                'success': False,
                            })
                    except Exception as e:
                        return Response({
                            'message': str(e),
                            'status': status.HTTP_400_BAD_REQUEST,
                            'success': False,
                        })
                else:
                    return Response({
                            'message': 'please select phone or email',
                            'status': status.HTTP_400_BAD_REQUEST,
                            'success': False,
                        })
            else:
                return Response({
                   'message': 'User_id is required',
                    'status': status.HTTP_400_BAD_REQUEST,
                    'success': False,
                })
        elif request.data.get('section') == 'login':

            phone_or_email=request.data.get('phone_or_email')
            if phone_or_email=="phone":
                try:
                    phone_number = request.data.get('phone')
                    otp = request.data.get('otp')
                    if phone_number and otp:
                        phone = str(phone_number)
                        user = User.objects.filter(phone=phone).first()
                        if user:
                            data = user
                            if data.phone_otp == otp:
                                login(request, data)
                                data.phone_verified = True
                                data.save()
                                token = AuthToken.objects.create(data)
                                serializer = UserSerializer(data)
                                data = serializer.data
                                data['token'] = token[1]
                                response = [data]
                                return Response({
                                    'message': 'You Logged in successfully',
                                    'status': status.HTTP_200_OK,
                                    'success': True,
                                    'response': response
                                })
                            else:
                                return Response({
                                    'message': 'Phone OTP is incorrect',
                                    'status': status.HTTP_400_BAD_REQUEST,
                                    'success': False,
                                })

                        else:
                            return Response({
                                'message': 'Phone number not found',
                                'status': status.HTTP_404_NOT_FOUND,
                                'success': False,
                            }
                            )

                    else:
                        return Response({
                            'message': 'Phone number and OTP is required',
                            'status': status.HTTP_400_BAD_REQUEST,
                            'success': False,
                        })
                except Exception as e:
                    return Response({
                        'message': str(e),
                        'status': status.HTTP_400_BAD_REQUEST,
                        'success': False,
                    })
            elif phone_or_email=="email":
                try:
                    email = request.data.get('email')
                    otp = request.data.get('otp')

                    if email and otp:
                        user = User.objects.filter(email=email).first()
                        if user:
                            data = user
                            if data.email_otp == otp:
                                login(request, data)
                                data.email_verified = True
                                data.save()
                                token = AuthToken.objects.create(user)
                                serializer = UserSerializer(user)
                                data = serializer.data
                                data['token'] = token[1]
                                response = [data]
                                return Response({
                                    'message': 'You Logged in successfully',
                                    'status': status.HTTP_200_OK,
                                    'success': True,
                                    'response': response
                                })
                            else:
                                return Response({
                                    'message': 'Email OTP is incorrect',
                                    'status': status.HTTP_400_BAD_REQUEST,
                                    'success': False,
                                })
                        else:
                            return Response({
                                'message': 'Email-id is not found',
                                'status': status.HTTP_404_NOT_FOUND,
                                'success': False,
                            })
                    else:
                        return Response({
                            'message': 'Email and OTP is required',
                            'status': status.HTTP_400_BAD_REQUEST,
                            'success': False,
                        })
                except Exception as e:
                    return Response({
                        'message': str(e),
                        'status': status.HTTP_400_BAD_REQUEST,
                        'success': False,
                    })
            else:
                return Response({
                        'message': 'please select phone or email',
                        'status': status.HTTP_400_BAD_REQUEST,
                        'success': False,
                    })
        else:
                return Response({
                        'message': 'please select section',
                        'status': status.HTTP_400_BAD_REQUEST,
                        'success': False,
                    })
