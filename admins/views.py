from functools import partial
from http import server
from pydoc import Doc, doc
from this import d
from tkinter.messagebox import RETRY
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from .serializers import *
from doctor.serializers import DoctorSerializer
from .models import Speciality, Qualification
from admins.models import Location
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from .serializers import  LocationSerializer
from django.db.models import Q
from users.models import User
from doctor.models import DoctorRatingReview,Doctor
from users.serializers import DoctorRatingSerializer, UserSerializer
from django.db.models import Subquery


class GetAllReviewAPI(APIView):
    def get(self,request):
        rating = DoctorRatingReview.objects.filter(is_del = False   )
        serializer = RatingSerializer(rating,many=True)
        re = []
        data = {}
        for i in range(len(serializer.data)):
            data = dict(serializer.data[i])
            doctor = Doctor.objects.filter(id = data['doctor']).first()
            user = User.objects.filter(id = doctor.user_id_id).first()
            data['doctor'] = user.fname
            re.append(data)

        # userdata = dict(userserializer.data)
        # data = dict(serializer.data)
        # data['doctor'] = userdata['fname']
        return Response({
                                'message': 'all ratings - reviews',
                                'status': status.HTTP_200_OK,
                                'success': True,
                                'response': re
                            })
class BlockRatingAPI(APIView):
    def post(self,request):
        rating_id = request.data.get('rating_id')
        block = request.data.get('block')
        if rating_id and block:
            rating = DoctorRatingReview.objects.filter(Q(id = rating_id) & Q(is_del = False)).first()
            if rating:
                isBlock = block == '1'
                rating.is_blocked = isBlock
                rating.save()
                if isBlock == True:
                    return Response({
                                'message': 'rating - review Blocked Successfully',
                                'status': status.HTTP_200_OK,
                                'success': True,
                            })
                else:
                    return Response({
                                'message': 'rating - review Unblocked Successfully',
                                'status': status.HTTP_200_OK,
                                'success': True,
                            })
            else:
                return Response({'message':'rating - review is not found,please enter valid', 'status':status.HTTP_400_BAD_REQUEST,'success': False})
        else:
            if rating_id is None:
                return Response({'message':'rating_id is required', 'status':status.HTTP_400_BAD_REQUEST,'success': False})
            if block is None:
                return Response({'message':'block  is required', 'status':status.HTTP_400_BAD_REQUEST,'success': False})

class BlockVerifyAPIView(APIView):
    def post(self,request):
        user_id = request.data.get('user_id')
        block_or_verify = request.data.get('block_or_verify')
        if user_id and block_or_verify:
            user = User.objects.filter(Q(id = user_id) & Q(is_del = False)).first()
            if block_or_verify == 'block':
                block = request.data.get('is_blocked')
                if block:
                    if user:
                        isBlock = block == "1"
                        user.is_blocked = isBlock
                        user.save()
                        if isBlock == True:
                            return Response({
                                'message': 'User Blocked Successfully',
                                'status': status.HTTP_200_OK,
                                'success': True,
                            })
                        else:
                            return Response({
                                'message': 'User Unblocked Successfully',
                                'status': status.HTTP_200_OK,
                                'success': True,
                            })
                    else:
                        return Response({
                        'message': 'User not found',
                        'status': status.HTTP_404_NOT_FOUND,
                        'success': False,
                    })
                else:
                    return Response({
                        'message': 'is_blocked is required',
                        'status': status.HTTP_404_NOT_FOUND,
                        'success': False,
                        })
            elif block_or_verify == 'verify':
                verify = request.data.get('is_verified')
                if verify:
                    if user:
                        isVerify = verify == "1"
                        user.is_verified = isVerify
                        user.save()
                        if isVerify == True:
                            return Response({
                                'message': 'User Verified Successfully',
                                'status': status.HTTP_200_OK,
                                'success': True,
                            })
                        else:
                            return Response({
                                'message': 'User Unverified Successfully',
                                'status': status.HTTP_200_OK,
                                'success': True,
                            })
                    else:
                        return Response({
                        'message': 'User not found',
                        'status': status.HTTP_404_NOT_FOUND,
                        'success': False,
                    })
                else:
                    return Response({
                        'message': 'is_verified is required',
                        'status': status.HTTP_404_NOT_FOUND,
                        'success': False,
                        })
            else:
                return Response({
                        'message': 'please select block_or_verify',
                        'status': status.HTTP_404_NOT_FOUND,
                        'success': False,
                        })
        else:
            if user_id is None:
                return Response({
                'message': 'user_id is required',
                'status': status.HTTP_404_NOT_FOUND,
                'success': False,
            })
            if block_or_verify is None:
                return Response({
                'message': 'please select block_or_verify',
                'status': status.HTTP_404_NOT_FOUND,
                'success': False,
            })

# Create your views here.
class GetLocationAPIView(APIView):
    def get(self, request):
        try:
            section = Location.objects.filter(is_del=False)
            serializer = LocationSerializer(section, many=True)
            return Response({
            'status':status.HTTP_302_FOUND,
            'success':True,
            'responce':serializer.data
            })
        except Exception as e:
            return Response({
                'status':status.HTTP_400_BAD_REQUEST,
                'message':str(e)
            })

class OneLocationAPIView(APIView):
    def get(self, request):
        try:
            pk = request.data.get('location_id')
            if pk:
                data = Location.objects.filter(Q(id = pk) & Q(is_del = False)).first()
                if data:
                    serializer = LocationSerializer(data)
                    return Response({
                        'status': status.HTTP_302_FOUND,
                        'success': True,
                        'responce': serializer.data
                    })
                else:
                    return Response({
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': 'location is not found, please enter Valid Speciality',
                })
            else:
                return Response({
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': 'location_id is required',
                })
        except Exception as e:
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': str(e)
            })

class CreateLocationAPIView(APIView):
    
    def post(self, request):
        
            name = request.data.get('name')
            section=request.data.get('section')
            
            if section != 'state' and section!=None:
                category=request.data.get('is_cat')
                if category is None:
                    return Response({
                        'message' : 'Category_id field is required'
                    })
            if name and section:
                
                    state = Location.objects.filter(name = name).first()
                    
                    if state:
                        print(state)
                        if section=='state':
                            return Response({
                                'message':'state already exists',
                                'status':status.HTTP_400_BAD_REQUEST,
                                'success':False,
                                
                            })
                        if section=='city':
                            return Response({
                                'message':'city already exists',
                                'status':status.HTTP_400_BAD_REQUEST,
                                'success':False,
                                
                            })
                        if section=="area":
                            return Response({
                                'message':'area already exists',
                                'status':status.HTTP_400_BAD_REQUEST,
                                'success':False,
                                
                            })
                    else:
                        if section == 'area':
                            if request.data.get('area_section'):
                                serializer = LocationSerializer(data = request.data)
                        # if data["section"]=="state":
                        #         print('yes its state')
                                if serializer.is_valid():
                                    serializer.save()
                                    data = serializer.data
                                    if data["section"]=="area":
                                        return Response({
                                            'message':'area created successfully',
                                            'status':status.HTTP_201_CREATED,
                                            'success':True,
                                            'responce':{
                                                'id':data['id'],
                                                'name':data['name']
                                        }
                                        })
                                else:
                                    if serializer.errors:
                                        for i in reversed(serializer.errors):
                                            er = f"{i} is Required"
                                        return Response({'message':er, 'status':status.HTTP_400_BAD_REQUEST,'success': False})
                            
                            else:
                                return Response({
                                                'message': 'Area section field is required',
                                                'status':status.HTTP_400_BAD_REQUEST,
                                                'success':False   
                                                })
                        serializer = LocationSerializer(data = request.data)
                        # if data["section"]=="state":
                        #         print('yes its state')
                        if serializer.is_valid():
                            serializer.save()
                            data = serializer.data
                            # print(data["section"])
                            
                            
                            # print(data)
                            if data["section"]=="area":
                                return Response({
                                    'message':'area created successfully',
                                    'status':status.HTTP_201_CREATED,
                                    'success':True,
                                    'responce':{
                                        'id':data['id'],
                                        'name':data['name']
                                }
                            })
                            if data["section"]=="state":
                                return Response({
                                    'message':'state created successfully',
                                    'status':status.HTTP_201_CREATED,
                                    'success':True,
                                    'responce':{
                                        'id':data['id'],
                                        'name':data['name']
                                }
                            })
                            if data["section"]=="city":
                                return Response({
                                    'message':'city created successfully',
                                    'status':status.HTTP_201_CREATED,
                                    'success':True,
                                    'responce':{
                                        'id':data['id'],
                                        'name':data['name']
                                }
                            })
                            
                                
                        else:
                            if serializer.errors:
                                for i in reversed(serializer.errors):
                                    er = f"{i} is Required"
                                    return Response({'message':er, 'status':status.HTTP_400_BAD_REQUEST,'success': False})
               

            else:
                if name==None:
                    return Response({
                        'message': 'name field is required',
                        'status':status.HTTP_400_BAD_REQUEST,
                        'success':False   
                    })
                if section==None:
                    return Response({
                        'message': 'section field is required',
                        'status':status.HTTP_400_BAD_REQUEST,
                        'success':False   
                    })
               
            
            
#####################################################################################################
          
        # except Exception as e:
        #     return Response({
        #         'status':status.HTTP_400_BAD_REQUEST,
        #         'message':str(e)
        #     })

class UpdateLocationAPIView(APIView):
    def put(self, request):
        pk = request.data.get('location_id')
        if pk:
            lo = Location.objects.get(id=pk)
            state = request.data.get('name')
            section=request.data.get('section')
            if section != 'state' and section!=None:
                category=request.data.get('is_cat')
                if category is None:
                    return Response({
                        'message' : 'Category_id field is required'
                    })
            if state and section:
                lt = Location.objects.filter(name=state).first()
                if lt:
                    return Response({
                        'message':f'{state} already exists',
                        'status':status.HTTP_400_BAD_REQUEST,
                        'success':False
                    })
                else:
                    serializer = LocationSerializer(lo, data = request.data, partial=True)
                    if serializer.is_valid():
                        serializer.save()
                        data = serializer.data
                        return Response({
                            'message':f'{section} updated successfully',
                            'status':status.HTTP_200_OK,
                            'success':True,
                            'responce':{
                                'id':data['id'],
                                'name':data['name']
                            }
                        })  
                    else:
                        if serializer.errors:
                            for i in reversed(serializer.errors):
                                er = f"{i} is Required"
                            return Response({'message':er, 'status':status.HTTP_400_BAD_REQUEST,'success': False})                  
            else:
                if state is None:
                    return Response({
                        'message': 'name field is required',
                        'status':status.HTTP_400_BAD_REQUEST,
                        'success':False   
                    })
                if section is None:
                    return Response({
                        'message': 'section field is required',
                        'status':status.HTTP_400_BAD_REQUEST,
                        'success':False   
                    })
        else:
            return Response({
                        'message': 'location_id field is required',
                        'status':status.HTTP_400_BAD_REQUEST,
                        'success':False   
                    })
        # except Exception as e:
        #     return Response({
        #         'status':status.HTTP_400_BAD_REQUEST,
        #         'message':str(e)
        #     })

class DeleteLocationAPIView(APIView):
    def delete(self, request):
        try:
            pk = request.data.get('location_id')
            if pk:
                state = Location.objects.get(id=pk)
                if state.is_del == False:
                    state.is_del = True
                    state.save()
                    return Response({
                        'message':'your data is deleted successfully !',
                        'success': True,
                        'status':status.HTTP_301_MOVED_PERMANENTLY
                    })
                else:
                    return Response({
                        'message':'Already deleted !',
                        'success': False,
                        'status':status.HTTP_404_NOT_FOUND
                    })   
            else:
                 return Response({
                        'message':'location_id is required',
                        'success': False,
                        'status':status.HTTP_404_NOT_FOUND
                    })        
        except :
            return Response({
                    'message':'This ID not found !',
                    'success': False,
                    'status':status.HTTP_404_NOT_FOUND
                }) 



class CreateSpecialityAPIView(APIView):
    def post(self, request):
        try:
            speciaity_name = request.data.get('name')
            speciaity_icon = request.data.get('icon')
            if speciaity_name or speciaity_icon:
                name = Speciality.objects.filter(name=speciaity_name)
                if name.exists():
                    return Response({
                        'message': 'Speciality already exists',
                        'status': status.HTTP_400_BAD_REQUEST,
                        'success': False
                    })
                else:
                    speciality = Speciality.objects.create(
                        name=speciaity_name, icon=speciaity_icon)
                    return Response({
                        'message': 'Speciality created successfully',
                        'status': status.HTTP_201_CREATED,
                        'success': True,
                        'data': SpecialitySerializer(speciality).data
                    })
            else:
                return Response({
                    'message': 'Name is Required',
                    'status': status.HTTP_400_BAD_REQUEST,
                    'success': False
                })

        except Exception as e:
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': str(e)
            })

class OneSpecialityAPIView(APIView):
    def get(self, request):
        try:
            pk = request.data.get('speciality_id')
            if pk:
                data = Speciality.objects.filter(Q(id = pk) & Q(is_del = False)).first()
                if data:
                    serializer = SpecialitySerializer(data)
                    return Response({
                        'status': status.HTTP_302_FOUND,
                        'success': True,
                        'responce': serializer.data
                    })
                else:
                    return Response({
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': 'speciality is not found, please enter Valid Speciality',
                })
            else:
                return Response({
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': 'speciality_id is required',
                })
        except Exception as e:
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': str(e)
            })

class SpecialityAPIView(APIView):
    def get(self, request):
        try:
            data = Speciality.objects.filter(is_del=False)
            serializer = SpecialitySerializer(data, many=True)
            return Response({
                'status': status.HTTP_302_FOUND,
                'success': True,
                'responce': serializer.data
            })
        except Exception as e:
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': str(e)
            })


class UpdateSpecialityAPIView(APIView):
    def put(self, request,):
        try:
            pk = request.data.get('speciality_id')
            if pk:
                speciality = Speciality.objects.get(id=pk)
                serializer = SpecialitySerializer(speciality, data=request.data)
                speciality_name = request.data.get('name')
                if speciality_name:
                    name = Speciality.objects.filter(name=speciality_name)
                    if name.exists():
                        return Response({
                            'message': 'Speciality already exists',
                            'status': status.HTTP_400_BAD_REQUEST,
                            'success': False
                        })

                    elif serializer.is_valid():
                        serializer.save()
                        return Response({
                            'message': 'Speciality updated successfully',
                            'status': status.HTTP_200_OK,
                            'success': True,
                            'data': serializer.data
                        })
                    else:
                        if serializer.errors:
                            for i in reversed(serializer.errors):
                                er = f"{i} is Required"
                            return Response({'message':er, 'status':status.HTTP_400_BAD_REQUEST,'success': False})
            else:
                return Response({
                            'message': 'speciality_id is required',
                            'status': status.HTTP_400_BAD_REQUEST,
                            'success': False
                        })
            
        except Exception as e:
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': str(e)
            })


class DeleteSpecialityAPIView(APIView):
    def delete(self, request):
        try:
            pk = request.data.get('speciality_id')
            if pk:
                speciality = Speciality.objects.get(id=pk)
                if speciality.is_del == False:
                    speciality.is_del = True
                    speciality.save()
                    return Response({
                        'message': 'the speciality has been deleted!',
                        'success': True,
                        'status': status.HTTP_204_NO_CONTENT
                    })
                else:
                    return Response({
                        'message': 'the speciality Already deleted!',
                        'success': False,
                        'status': status.HTTP_404_NOT_FOUND
                    })
            else:
                return Response({
                        'message': 'speciality_id is required',
                        'success': False,
                        'status': status.HTTP_404_NOT_FOUND
                    })

        except Exception as e:
            return Response({
                'success': False,
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': str(e),
            })


# CRUD Qualifications
class CreateQualificationAPIView(APIView):
    def post(self, request):
        try:
            qualification_name = request.data.get('name')
            if qualification_name:
                name = Qualification.objects.filter(name=qualification_name)
                if name.exists():
                    return Response({
                        'message': 'Qualification already exists',
                        'status': status.HTTP_400_BAD_REQUEST,
                        'success': False
                    })
                else:
                    qualification = Qualification.objects.create(
                        name=qualification_name)
                    return Response({
                        'message': 'Qualification created successfully',
                        'status': status.HTTP_201_CREATED,
                        'success': True,
                        'data': QualificationSerializer(qualification).data
                    })
            else:
                return Response({
                    'message': 'Name is Required',
                    'status': status.HTTP_400_BAD_REQUEST,
                    'success': False
                })
        except Exception as e:
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': str(e)
            })

class OneQualificationAPIView(APIView):
    def get(self, request):
        try:
            pk = request.data.get('qualification_id')
            if pk:
                data = Qualification.objects.filter(Q(id = pk) & Q(is_del = False)).first()
                if data:
                    serializer = QualificationSerializer(data)
                    return Response({
                        'status': status.HTTP_302_FOUND,
                        'success': True,
                        'responce': serializer.data
                    })
                else:
                    return Response({
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': 'qualification is not found, please enter Valid Speciality',
                })
            else:
                return Response({
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': 'qualification_id is required',
                })
        except Exception as e:
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': str(e)
            })

class GetQualificationsAPIView(APIView):
    def get(self, request):
        try:
            data = Qualification.objects.filter(is_del=False)
            serializer = QualificationSerializer(data, many=True)
            return Response({
                'status': status.HTTP_302_FOUND,
                'success': True,
                'response': serializer.data
            })
        except Exception as e:
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': str(e)
            })


class UpdateQualificationAPIView(APIView):
    def put(self, request):
        try:
            pk = request.data.get('qualification_id')
            if pk:
                qualification = Qualification.objects.get(id=pk)
                serializer = QualificationSerializer(
                    qualification, data=request.data)
                qualification_name = request.data.get('name')
                if qualification_name:
                    name = Qualification.objects.filter(name=qualification_name)
                    if name.exists():
                        return Response({
                            'message': 'Qualification already exists',
                            'status': status.HTTP_400_BAD_REQUEST,
                            'success': False
                        })
                    elif serializer.is_valid():
                        serializer.save()
                        return Response({
                            'message': 'Qualification updated successfully',
                            'status': status.HTTP_200_OK,
                            'success': True,
                            'data': serializer.data
                        })
                    else:
                        if serializer.errors:
                            for i in reversed(serializer.errors):
                                er = f"{i} is Required"
                            return Response({'message':er, 'status':status.HTTP_400_BAD_REQUEST,'success': False})
            else:
                return Response({
                        'message': 'qualification_id is required',
                        'status': status.HTTP_400_BAD_REQUEST,
                        'success': False
                    })
        except Exception as e:
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': str(e)
            })


class DeleteQualificationAPIView(APIView):
    def delete(self, request):
        try:
            pk = request.data.get('qualification_id')
            if pk:
                data = Qualification.objects.get(id=pk)
                if data.is_del == False:
                    data.is_del = True
                    data.save()
                    return Response({
                        'message': 'The Qulification has been deleted!',
                        'success': True,
                        'status': status.HTTP_204_NO_CONTENT
                    })
                else:
                    return Response({
                        'message': 'The Qulification Already deleted!',
                        'success': False,
                        'status': status.HTTP_404_NOT_FOUND
                    })
            else:
                return Response({
                        'message': 'qualification_id is required',
                        'success': False,
                        'status': status.HTTP_404_NOT_FOUND
                    })
        except Exception as e:
            return Response({
                'success': False,
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': str(e),
            })


