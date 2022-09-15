from functools import partial
from multiprocessing import managers
from pydoc import Doc
from sys import api_version
from urllib import response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics ,permissions
from knox.models import AuthToken
from sqlalchemy import union
from users.models import Roles, TempData
from users.serializers import RoleSerializer, TempDataSerializer, RegisterSerializer, UserSerializer , ViewUserSerializer , DoctorRatingSerializer
from users.utils import send_phone_otp,send_email_otp
from django.contrib.auth import get_user_model ,login
from rest_framework import viewsets
from django.db.models import Q
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.models import Q
from doctor.models import Doctor,DoctorRatingReview

User = get_user_model()

# Create your views here.
@api_view(['PUT','PATCH'])
@csrf_exempt
def edituser(request):
    if request.method == 'PUT' or request.method == 'PATCH':
        user_id = request.data.get('user_id')
        phone = request.data.get('phone')
        email = request.data.get('email')
        if user_id and phone and email:
            phone = str(phone)
            user = User.objects.filter(id = user_id).first()
            if user:
                phonec = Q(phone = phone)
                phonev = Q(phone_verified = True)
                emailc = Q(email = email)
                emailv = Q(email_verified = True)
                tempp = TempData.objects.filter(phonec & phonev).first()
                tempe = TempData.objects.filter(emailc & emailv).first()
                if tempp and tempe:
                    serializer = RegisterSerializer(user,data= request.data,partial=True)
                    if serializer.is_valid():
                        serializer.save()
                        dic = serializer.data
                        response = [dic]    
                        return Response({
                        'message': 'User edited successfully',
                        'status': status.HTTP_200_OK,
                        'success': True,
                        "response": response,    
                    })
                    else:
                        if serializer.errors:
                            for i in reversed(serializer.errors):
                                er = f"{i} is Required"
                                return Response({'message':er, 'status':status.HTTP_400_BAD_REQUEST,'success': False})
                else:
                    return Response({'message ':'please verify phone and email', 
                            'status':'status.HTTP_400_BAD_REQUEST','success': False })

            else:
                return Response({'message ':'user not found,Please Register First', 
                            'status':'status.HTTP_400_BAD_REQUEST','success': False })
        else:
            if user_id is None:
                return Response({'message ':'user_id fields is required', 
                            'status':'status.HTTP_400_BAD_REQUEST','success': False })
            if phone is None:
                return Response({'message ':'phone fields is required', 
                            'status':'status.HTTP_400_BAD_REQUEST','success': False })
            if email is None:
                return Response({'message ':'email fields is required', 
                            'status':'status.HTTP_400_BAD_REQUEST','success': False })

class CreateRatingAPI(APIView):
    def post(self,request):
        user_id = request.data.get('user')
        doctor_id = request.data.get('doctor')
        if user_id and doctor_id:
            user = User.objects.filter(Q(id = user_id) & Q(is_verified = True)).first()
            doctor = Doctor.objects.filter(id = doctor_id).first()
            if user and doctor:
                serializer = DoctorRatingSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    data = serializer.data
                    return Response({
                            'message': 'rating - review created successfully',
                            'status': status.HTTP_200_OK,
                            'success': True,
                            "response": data,    
                                })
                else:
                    if serializer.errors:
                        for i in reversed(serializer.errors):
                            er = f"{i} is Required"
                        return Response({'message':er, 'status':status.HTTP_400_BAD_REQUEST,'success': False})
            else:
                if user is None:
                    return Response({'message':'verified is not found,please enter verified user', 'status':status.HTTP_400_BAD_REQUEST,'success': False})
                if doctor is None:
                    return Response({'message':'doctor is not found,please enter valid doctor', 'status':status.HTTP_400_BAD_REQUEST,'success': False})
        else:
            if user_id is None:
                return Response({'message':'user is required', 'status':status.HTTP_400_BAD_REQUEST,'success': False})
            if doctor_id is None:
                return Response({'message':'doctor is required', 'status':status.HTTP_400_BAD_REQUEST,'success': False})

@api_view(['PUT','PATCH'])
def EditRating(request):
    if request.method == 'PUT' or request.method == 'PATCH':
        rating_id = request.data.get('rating_id')
        if rating_id:
            rating = DoctorRatingReview.objects.filter(Q(id = rating_id) & Q(is_del = False)).first()
            if rating:
                serializer = DoctorRatingSerializer(rating,request.data,partial=True)
                if serializer.is_valid():
                    serializer.save()
                    data = serializer.data
                    return Response({
                            'message': 'rating - review edited successfully',
                            'status': status.HTTP_200_OK,
                            'success': True,
                            "response": data,    
                            })
                else:
                    return Response({'message':serializer.errors, 'status':status.HTTP_400_BAD_REQUEST,'success': False})
            else:
                return Response({'message':'rating - reivew is not found,please enter valid', 'status':status.HTTP_400_BAD_REQUEST,'success': False})
        else:
            return Response({'message':'rating_id is required', 'status':status.HTTP_400_BAD_REQUEST,'success': False})
class RoleAPIView(APIView):
    def get(self, request):
        roles = Roles.objects.all()
        serializer = RoleSerializer(roles, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TempDataAPIView(APIView):
    def get(self, request):
        temp_data = TempData.objects.all()
        serializer = TempDataSerializer(temp_data, many=True)
        return Response(serializer.data)

    def post(self, request):
        phone = request.data.get('phone')
        email = request.data.get('email')
        if phone and email:
            ptemp = TempData.objects.filter(phone = phone).first()
            etemp = TempData.objects.filter(email=email).first()
            if ptemp:
                return Response({'message ':'phone is already exist', 
                            'status':'status.HTTP_400_BAD_REQUEST','success': False })
            elif etemp:
                return Response({'message ':'email is already exist', 
                            'status':'status.HTTP_400_BAD_REQUEST','success': False })
            else:
                serializer = TempDataSerializer(data=request.data)
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
            return Response({'message ':'phone and email required', 
                            'status':'status.HTTP_400_BAD_REQUEST','success': False })
    



class SignUpAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    
    def post(self, request, *args, **kwargs):
            email = request.data.get('email')
            phone = request.data.get('phone')
            if email is None:
                return Response({'message':'email is required', 'status':status.HTTP_400_BAD_REQUEST,'success': False})
            if phone is None:
                return Response({'message':'phone is required', 'status':status.HTTP_400_BAD_REQUEST,'success': False})
            else:
                if len(phone) < 8 or len(phone) > 15:
                    return Response({'message':'phone length should be 9 to 15', 'status':status.HTTP_400_BAD_REQUEST,'success': False})
            user = User.objects.filter(Q(email = email) | Q(phone = phone))
            if user:
                user = User.objects.filter(phone = phone).first()
                if user:
                    return Response({'message':'phone already exist', 'status':status.HTTP_400_BAD_REQUEST,'success': False})
                user = User.objects.filter(email = email).first()
                if user:
                    return Response({'message':'email already exist', 'status':status.HTTP_400_BAD_REQUEST,'success': False})
            else:
                phonec = Q(phone = phone)
                phonev = Q(phone_verified = True)
                emailc = Q(email = email)
                emailv = Q(email_verified = True)
                tempp = TempData.objects.filter(phonec & phonev).first()
                tempe = TempData.objects.filter(emailc & emailv).first()
                if tempp and tempe:
                    serializer = RegisterSerializer(data=request.data)
                    if serializer.is_valid():
                        user.is_verified = True
                        
                        # user.save()
                        user = serializer.save()
                        print(user)
                        data = serializer.data
                        token = AuthToken.objects.create(user)
                        data['token'] = token[1]
                        response = [data]
                        return Response({
                        'message': 'User created successfully',
                        'status': status.HTTP_200_OK,
                        'success': True,
                        "response": response,    
                    })
                    else:
                        if serializer.errors:
                            for i in reversed(serializer.errors):
                                er = f"{i} is Required"
                        return Response({'message':er, 'status':status.HTTP_400_BAD_REQUEST,'success': False})
                else:
                    if tempp is None:
                        return Response({'message':'Please Verify Your phone', 'status':status.HTTP_400_BAD_REQUEST,'success': False})
                    if tempe is None:
                        return Response({'message':'Please Verify Your Email', 'status':status.HTTP_400_BAD_REQUEST,'success': False})
    
class GetUsersAPIView(APIView):
    serializer_class = RegisterSerializer
    def get(self,request,*args,**kwargs):
        user = User.objects.filter(is_del = False)
        if user.exists():
            serializer = ViewUserSerializer(user,many = True)
            data = serializer.data
            response = data
            return Response({'status': status.HTTP_200_OK,'success': True,"response": response,})
        else:
            return Response({'message':'user not found', 'status':status.HTTP_400_BAD_REQUEST,'success': False})

# get auth user
class GetAuthUserAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated,]
    def get(self, request, *args, **kwargs):
        user = request.user
        if user:
            return Response({
                'message': 'User Get Successfully',
                'status': status.HTTP_200_OK,
                'success': True,
                "response": {
                    'id': user.id,
                    'name' : str(user.fname) + ' ' + str(user.lname),
                    'email': user.email,
                    'phone': user.phone,
                    'address': user.address,
                }
            })
        else:
            return Response({
                'message': 'User not found',
                'status': status.HTTP_404_NOT_FOUND,
                'success': False,
            })
    
# send otp for login user profile

class UserLogoutAPIView(APIView):
    def post(self,request,*args,**kwargs):
        token = request.data.get('token')
        if token:
            dbtoken = AuthToken.objects.filter(digest = token).first()
            if dbtoken:
                dbtoken.delete()
                return Response({
                            'message': 'user logout successfully',
                            'status': status.HTTP_200_OK,
                            'success': True,
                        }) 
            else:
                return Response({
                'message': 'token not found,please enter valid token',
                'status': status.HTTP_404_NOT_FOUND,
                'success': False,
            })
        else:
            return Response({
                'message': 'token is required',
                'status': status.HTTP_404_NOT_FOUND,
                'success': False,
            })
class LoginPhoneSendAPI(APIView):
    def post(self, request, *agrs, **kwargs):
        try:
            phone_number = request.data.get('phone')
            if phone_number:
                phone = str(phone_number)
                user = User.objects.filter(phone__iexact=phone)
                if user.exists():
                    data = user.first()
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
                    'message': 'Phone number is required ! please check your input',
                    'status': status.HTTP_400_BAD_REQUEST,
                    'success': False,
                })

        except Exception as e:
            return Response({
                'message': str(e),
                'status': status.HTTP_400_BAD_REQUEST,
                'success': False,
            })


class LoginPhoneVerifyAPI(APIView):
    def post(self, request, *agrs, **kwargs):
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
                        'message': 'User with this Phone number is not found',
                        'status': status.HTTP_404_NOT_FOUND,
                        'success': False,
                    })
            else:
                return Response({
                        'message': 'phone and otp are required',
                        'status': status.HTTP_404_NOT_FOUND,
                        'success': False,
                })
        except Exception as e:
            return Response({
                'message': str(e),
                'status': status.HTTP_400_BAD_REQUEST,
                'success': False,
            })
                        