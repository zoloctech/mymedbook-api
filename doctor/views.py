import pickle
from pydoc import doc
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from rest_framework.response import Response
from rest_framework.views import APIView
import datetime 
from uuid import uuid4
from google.auth.transport.requests import Request
from pathlib import Path
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, generics
from .models import Speciality, Qualification, Doctor, DoctorTiming
from .serializers import *
from rest_framework import permissions
from django.db.models import Q
from googleapiclient.discovery import build
from rest_framework.decorators import api_view
from users.models import User
from django.views.decorators.csrf import csrf_exempt
import datetime
from api.views import CreateCalendarEventAPIView
# from .meet_link import *
# Create your views here.


@api_view(['PUT','PATCH'])
@csrf_exempt
def editdoctor(request):
    if request.method == 'PUT' or request.method == 'PATCH':
        doctor_id = request.data.get('doctor_id')
        if doctor_id:
            user = Doctor.objects.filter(id = doctor_id).first()
            if user:
                serializer = DoctorSerializer(user,data= request.data,partial=True)
                if serializer.is_valid():
                    serializer.save()
                    dic = serializer.data
                    response = [dic]    
                    return Response({
                    'message': 'Doctor edited successfully',
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
                return Response({'message ':'Doctor not found,Please Register First', 
                                'status':'status.HTTP_400_BAD_REQUEST','success': False })
        else:
            return Response({
                    'message': 'Doctor_id is required',
                    'status': status.HTTP_200_OK,
                    'success': True, 
                })

class ViewAllDoctorsAPIView(APIView):
    serializer_class = ViewDoctorSerializer
    def get(self,request,*args,**kwargs):
        
        doctor = Doctor.objects.filter(is_del = False)
        if doctor.exists():
            serializer = ViewDoctorSerializer(doctor,context={'request': request},many = True)
            data = serializer.data
            response = data
            return Response({'status': status.HTTP_200_OK,'success': True,"response": response,})
        else:
            return Response({'message':'user not found', 'status':status.HTTP_400_BAD_REQUEST,'success': False})

class CreateDoctorAPIView(APIView):
    parser_classes = (MultiPartParser, )
    serializer_class = DoctorSerializer
    def post(self, request, *args, **kwargs):
            user_id = request.data.get('user_id')
            if user_id:
                user = User.objects.filter(id = user_id).first()
            else:
                return Response({
                    'message':'user_id is required', 'status':status.HTTP_400_BAD_REQUEST,'success': False
                })
            if user:
                user.is_verified = False
                user.save()
                serializer = DoctorSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    data = serializer.data
                    response = [data]
                    return Response({
                    'message': 'Doctor created successfully',
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
                return Response({
                    'message':'User not found,please enter valid user_id', 'status':status.HTTP_400_BAD_REQUEST,'success': False
                })
                
                
# get a doctor by id
class GetDoctorAPIView(APIView):
    def get(self,request,pk):
        doctor = Doctor.objects.filter(id = pk).first()
        if doctor:
            serializer = ViewDoctorSerializer(doctor,context={'request': request})
            data = serializer.data
            response = [data]
            return Response({'status': status.HTTP_200_OK,'success': True,"response": response,})
        else:
            return Response({'message':'Doctor not found', 'status':status.HTTP_400_BAD_REQUEST,'success': False})

# take doctor_id and return doctor details
class TakeAppointment(APIView):
    serializer_class=AppointmentSerializer
    def post(self,request, *args, **kwargs):
        Doctor_id= request.data.get('doctor_id')
        start_date=request.data.get('start_date')
        end_date=request.data.get('end_date')
        start_time=request.data.get('start_time')
        end_time=request.data.get('end_time')
        if Doctor_id and start_date and end_date and start_time and end_time:
            user_id=request.data.get('user_id') 
            formatdate = '%Y/%m/%d'
            start_date = datetime.datetime.strptime(start_date, formatdate).date()
            end_date = datetime.datetime.strptime(end_date, formatdate).date()
            formattime = '%H:%M:%S'
            start_time = datetime.datetime.strptime(start_time,formattime).time()
            end_time = datetime.datetime.strptime(end_time,formattime).time()
            appointment = Appointment.objects.filter(Q(doctor_id = Doctor_id) & Q(start_date = start_date))
            doctor = Doctor.objects.filter(id = Doctor_id).first()
            user = User.objects.filter(id = doctor.user_id_id).first()
            if appointment:
                return Response({
                    'message': 'Doctor not available at your time,select another time',
                        'status': status.HTTP_400_BAD_REQUEST,
                        'success': False,
                })
            else:
                if start_date > end_date:
                    return Response({
                    'message': 'please enter valid end date',
                        'status': status.HTTP_400_BAD_REQUEST,
                        'success': False,
                })
                else:
                    # ts = str(start_time.ts)
                    # te = str(end_time.te)
                    # diff=datetime.strptime(te, formattime)-datetime.strptime(ts, formattime)
                    # print(diff.seconds / 3600)
                    doctor = Doctor.objects.filter(id = Doctor_id).first()
                    if doctor:
                        createAppointment = Appointment(doctor_id = Doctor_id,user_id = user_id,start_date = start_date,start_time = start_time,end_date = end_date,end_time = end_time)
                        createAppointment.save()
                        response = {'doctor' : user.fname,'start_date' : start_date,'start_time' : start_time,'end_date' : end_date,'end_time':end_time}
                        return Response({
                            'message': 'Your Appointment is booked',
                            'status': status.HTTP_200_OK,
                            'success': True,
                            "response": response,
                        })
                    else:
                        return Response({
                        'message': 'doctor not found,please select valid doctor',
                        'status': status.HTTP_400_BAD_REQUEST,
                        'success': False,})
            

        if Doctor_id is None:
          return  Response({
                 'message':'Doctor_id is required.',
                 'status':status.HTTP_400_BAD_REQUEST,
                 'success': False})

        if start_date is None:
            return  Response({
                 'message':'Start_date is required.',
                 'status':status.HTTP_400_BAD_REQUEST,
                 'success': False})

        if end_date is None:
            return  Response({
                 'message':'end_date is required.',
                 'status':status.HTTP_400_BAD_REQUEST,
                 'success': False})
        
        if start_time is None:
            return  Response({
                 'message':'start_time is required.',
                 'status':status.HTTP_400_BAD_REQUEST,
                 'success': False})

        if end_time is None:
            return  Response({
                 'message':'end_time is required.',
                 'status':status.HTTP_400_BAD_REQUEST,
                 'success': False})

class DoctorCalandarSchedule(APIView):
     def post(self,request, *args, **kwargs):
        Doctor_id= request.data.get('doctor_id')
        start_date=request.data.get('start_date')
        end_date=request.data.get('end_date')
        start_time=request.data.get('start_time')
        end_time=request.data.get('end_time')
        if Doctor_id and start_date and end_date and start_time and end_time:
            user_id=request.data.get('user_id') 
            formatdate = '%Y/%m/%d'
            start_date = datetime.datetime.strptime(start_date, formatdate).date()
            end_date = datetime.datetime.strptime(end_date, formatdate).date()
            dr=DoctorTiming.objects.filter(Q(doctor_id = Doctor_id) & Q(start_date = start_date)).last()
            formattime = '%H:%M:%S'
            start_time = datetime.datetime.strptime(start_time,formattime).time()
            end_time = datetime.datetime.strptime(end_time,formattime).time()
            doctor = Doctor.objects.filter(id = Doctor_id).first()
            if doctor:
                user = User.objects.filter(id = doctor.user_id_id).first()
                schedul = DoctorTiming.objects.filter(Q(doctor_id = Doctor_id) & Q(start_date = start_date) & Q(start_time=start_time))
                if not schedul:
                    if doctor:
                        if start_date > end_date:
                            return Response({
                                'message': 'please enter valid end date',
                                'status': status.HTTP_400_BAD_REQUEST,
                                'success': False,
                        })
                        else:
                            if start_time >= end_time:
                                return Response({
                                        'message': 'please enter valid end time',
                                        'status': status.HTTP_400_BAD_REQUEST,
                                        'success': False,
                                    })
                            else:
                                app=DoctorTiming.objects.filter(Q(doctor_id = Doctor_id) & Q(start_date = start_date) & Q(end_time=end_time))
                                if app.exists():
                                    for i in app:
                                        if start_time < end_time:
                                            return Response({
                                                'message': 'this slot is booked',
                                                'status': status.HTTP_400_BAD_REQUEST,
                                                'success': False,
                                                })  
                                
                                else:
                                    if dr is None or start_time >= dr.end_time:
                                        createSchedule = DoctorTiming(doctor_id = Doctor_id,start_date = start_date,start_time = start_time,end_date = end_date,end_time = end_time)
                                        createSchedule.save()
                                        response = {'doctor' : user.fname,'start_date' : start_date,'start_time' : start_time,'end_date' : end_date,'end_time':end_time}
                                        print(response)
                                        return Response({
                                                'message': 'Doctor time schedule created successfully ',
                                                    'status': status.HTTP_200_OK,
                                                    'success': True,
                                                    'response': response,
                                            })
                                    else:
                                        return Response({
                                                'message': 'already fix ',
                                                    'status': status.HTTP_400_BAD_REQUEST,
                                                    'success': False,
                                            })

                    else:
                        return Response({
                                'message': 'some error..! please check once',
                                    'status': status.HTTP_400_BAD_REQUEST,
                                    'success': False,
                            })
                
                else:
                    return Response({
                        'message': 'Your schedule is alredy fixed',
                            'status': status.HTTP_400_BAD_REQUEST,
                            'success': False,
                    })
            else:
                return Response({
                 'message':'doctor not found,please select valid doctor_id',
                 'status':status.HTTP_400_BAD_REQUEST,
                 'success': False})
        if Doctor_id is None:
          return  Response({
                 'message':'Doctor_id is required.',
                 'status':status.HTTP_400_BAD_REQUEST,
                 'success': False})

        if start_date is None:
            return  Response({
                 'message':'Start_date is required.',
                 'status':status.HTTP_400_BAD_REQUEST,
                 'success': False})

        if end_date is None:
            return  Response({
                 'message':'end_date is required.',
                 'status':status.HTTP_400_BAD_REQUEST,
                 'success': False})
        
        if start_time is None:
            return  Response({
                 'message':'start_time is required.',
                 'status':status.HTTP_400_BAD_REQUEST,
                 'success': False})

        if end_time is None:
            return  Response({
                 'message':'end_time is required.',
                 'status':status.HTTP_400_BAD_REQUEST,
                 'success': False})

class BookAnAppointmentList(APIView):
     def post(self,request, *args, **kwargs):
       serializer_class=BookAnAppointmentSerializer
       mode=request.data.get('mode')
       doctor_id=request.data.get('doctor_id')
       patient_id = request.data.get('patient_id')
       start_date = request.data.get('start_date')
       formatdate = '%Y/%m/%d'
       start_time = request.data.get('start_time')
       print(type(start_time))
    #    end_time = start_time + timedelta(hours=4)
    #    timezone = 'Asia/Kolkata'
       formattime = '%H:%M:%S'
       doctor = Doctor.objects.filter(id = doctor_id).first()
       patient = User.objects.filter(id = patient_id).first()
       if mode and doctor_id and patient_id and start_date and start_time:
           if doctor:
               if patient:
                   if doctor_id == patient_id:
                       return Response ({
                           'message':'Please enter valid doctor_id and patient_id',
                           'status':status.HTTP_400_BAD_REQUEST,
                           'success': False})
                   else: 
                       if mode == "offline":
                           user = User.objects.filter(id = doctor_id).first()
                           url = request.data.get('url')
                           # serializer = BookAnAppointmentSerializer
                           # if serializer.is_valid():
                           #     serializer.save()
                           start_date = datetime.datetime.strptime(start_date, formatdate).date()
                           start_time = datetime.datetime.strptime(start_time,formattime).time()
                           createAppointment = BookAppointment(appointment_mode = mode, doctor_id = doctor_id,patient_id = patient_id, start_date = start_date,start_time = start_time, meeting_link = url)
                           createAppointment.save()
                           response = {'mode':mode, 'doctor' : user.fname,'patient_id': patient_id, 'start_date' : start_date,'start_time' : start_time,'url' : url}
                           return Response({
                               'message': 'Your Offline appointment created successfully ',
                                   'status': status.HTTP_200_OK,
                                   'success': True,
                                   'response': response,
                           })
                       if mode == "online":
                        meetObj = CreateCalendarEventAPIView()
                        res = meetObj.get(request)
                        print(res)
                        url = res['data']['hangout_url']
                        user = User.objects.filter(id = doctor_id).first()
                        start_date = datetime.datetime.strptime(start_date, formatdate).date()
                        start_time = datetime.datetime.strptime(start_time,formattime).time()
                        createAppointment = BookAppointment(appointment_mode = mode, doctor_id = doctor_id,patient_id = patient_id, start_date = start_date,start_time = start_time, meeting_link = url)
                        createAppointment.save()
                        response = {'mode':mode, 'doctor' : user.fname,'patient_id': patient_id, 'start_date' : start_date,'start_time' : start_time,'url' : url}
                        return Response({
                               'message': 'Your online appointment created successfully ',
                                   'status': status.HTTP_200_OK,
                                   'success': True,
                                   'response': response,
                           })
                       else:
                           return Response({
                               'message':'Failed to book an Appointment, Please Try Agaim',
                               'status':status.HTTP_400_BAD_REQUEST,
                               'success': False})
               else:
                   return Response({
                           'message':'Patient_id is not found , Please enter valid paintent_id',
                           'status':status.HTTP_400_BAD_REQUEST,
                           'success': False})
           else:
               return Response({
                       'message':'Doctor is not found , Please enter valid doctor_id',
                       'status':status.HTTP_400_BAD_REQUEST,
                       'success': False})
               
               
       if mode is None:
           return  Response({
                'message':'mode is required.',
                'status':status.HTTP_400_BAD_REQUEST,
                'success': False})
       if doctor_id is None:
           return  Response({
                'message':'doctor_id is required.',
                'status':status.HTTP_400_BAD_REQUEST,
                'success': False})
       if patient_id is None:
           return  Response({
                'message':'patient_id is required.',
                'status':status.HTTP_400_BAD_REQUEST,
                'success': False})
       if start_date is None:
           return  Response({
                'message':'start_date is required.',
                'status':status.HTTP_400_BAD_REQUEST,
                'success': False})
       if start_time is None:
           return  Response({
                'message':'start_time is required.',
                'status':status.HTTP_400_BAD_REQUEST,
                'success': False})
# Book appointment 
class BookAppointmentList(APIView):
    def post(self, request, *args, **kwargs):
       mode = request.data.get('mode')
       doctor_id = request.data.get('doctor_id')
       patient_id = request.data.get('patient_id')
       start_date = request.data.get('start_date')
       formatdate = '%Y/%m/%d'
       start_time = request.data.get('start_time')
       formattime = '%H:%M:%S'
       if mode and doctor_id and patient_id and start_date and start_time:
           if mode == "offline":
               url = None
               start_date = datetime.datetime.strptime(start_date, formatdate).date()
               start_time = datetime.datetime.strptime(start_time,formattime).time()
               createAppointment = BookAppointment(appointment_mode = mode, doctor_id = doctor_id,patient_id = patient_id, start_date = start_date,start_time = start_time, meeting_link = url)
               createAppointment.save()
               response = {'mode':mode, 'doctor_id' : doctor_id,'patient_id': patient_id, 'start_date' : start_date,'start_time' : start_time,'url' : url}
               return Response({
                   'message': 'Your Offline appointment created successfully ',
                       'status': status.HTTP_200_OK,
                       'success': True,
                       'response': response,
               })
           if mode == "online":
            start_date = datetime.datetime.strptime(start_date, formatdate).date()
            start_time = datetime.datetime.strptime(start_time,formattime).time()
            # print("start_date", start_date)
            # print(start_time)
            scopes = ['https://www.googleapis.com/auth/calendar']
            credentials = None
            token_file = Path("token.pickle")
            if token_file.exists():
                with open(token_file, "rb") as token:
                    credentials = pickle.load(token)
            if not credentials or not credentials.valid:
                if credentials and credentials.expired and credentials.refresh_token:
                    credentials.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file("credentials.json", scopes)
                    credentials = flow.run_local_server(port=0)
                    credentials.refresh(Request())
                with open(token_file, "wb") as token:
                    pickle.dump(credentials, token)

            calendar_service = build("calendar", "v3", credentials=credentials)
            event = {
                "summary": "Appointment",
                "start": {
                    "dateTime": str(start_date) + "T" + str(start_time),
                    "timeZone": "Asia/Kolkata",
                },
                "end": {
                    "dateTime": str(start_date) + "T" + str(start_time),
                    "timeZone": "Asia/Kolkata",
                },
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'email', 'minutes': 24 * 60},
                        {'method': 'popup', 'minutes': 10},
                    ],
                },
                'conferenceData': {
                    'createRequest': {
                        'requestId': f"{uuid4().hex}",
                        'conferenceSolutionKey': {
                            'type': 'hangoutsMeet',
                            'requestId': '123456789',
                        },
                    },
                },
            }
            event = calendar_service.events().insert(calendarId="primary", sendNotifications=True,body=event, conferenceDataVersion=1).execute()

            url = event.get('hangoutLink')
            appointment = BookAppointment(appointment_mode = mode, doctor_id = doctor_id,patient_id = patient_id, start_date = start_date,start_time = start_time, meeting_link = url)
            appointment.save()
            return Response({
                'message': 'Your Online appointment created successfully ',
                'status': status.HTTP_200_OK,
                'success': True,
                'response': {
                    "mode": mode,
                    "doctor_id": doctor_id,
                    "patient_id": patient_id,
                    "start_date": start_date,
                    "start_time": start_time,
                    "url": url
                }

            })



#get qualification by id
class GetQualificationDoctorAPIView(APIView):
    def post(self, request, *args, **kwargs):
        doctor_id = request.data.get('doctor_id')
        if doctor_id:
            try:
                data = Doctor.objects.get(id=doctor_id)
                return Response({
                    'message': 'Qualification of doctor',
                    'status': status.HTTP_200_OK,
                    'success': True,
                    'response': data.qualification_id.name,
                    })
                
            except Doctor.DoesNotExist:
                return Response({
                    'message': 'Doctor does not exist',
                    'status': status.HTTP_400_BAD_REQUEST,
                    'success': False,
                })
        else:
            return Response({
                'message': 'doctor_id is required',
                'status': status.HTTP_400_BAD_REQUEST,
                'success': False
            })
            
            
# get Specialization by id
class GetSPecializationDoctorAPIView(APIView):
    def post(self, request, *args, **kwargs):
        doctor_id = request.data.get('doctor_id')
        if doctor_id:
            try:
                data = Doctor.objects.get(id=doctor_id)
                return Response({
                    'message': 'Specialization of doctor',
                    'status': status.HTTP_200_OK,
                    'success': True,
                    'response': data.specilization_id.name,
                    })
                
            except Doctor.DoesNotExist:
                return Response({
                    'message': 'Doctor does not exist',
                    'status': status.HTTP_400_BAD_REQUEST,
                    'success': False,
                })
        else:
            return Response({
                'message': 'doctor_id is required',
                'status': status.HTTP_400_BAD_REQUEST,
                'success': False
            })