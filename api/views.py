from django.http import HttpResponse
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from rest_framework.response import Response
from rest_framework.views import APIView
import datetime
from uuid import uuid4
from pickle import load, dump
from google.auth.transport.requests import Request
from pathlib import Path
from rest_framework import status
# Create your views here.
def hell(request):
    return HttpResponse("Hello World")

# Path: api\views.py
class CreateCalendarEventAPIView(APIView):
    def get(self, request):
        mode=request.data.get('mode')
        if mode == "online":
            scopes = ['https://www.googleapis.com/auth/calendar']
            credentials = None
            token_file = Path("token.pickle")

            if token_file.exists():
                with open(token_file, "rb") as token:credentials = load(token)

            if not credentials or not credentials.valid:
                if credentials and credentials.expired and credentials.refresh_token:
                    credentials.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', scopes)
                    credentials = flow.run_local_server(port=0)
                with open(token_file, "wb") as token:
                    dump(credentials, token)

            calendar_service = build("calendar", "v3", credentials=credentials)

            # return Response(calendar_service)
            from datetime import datetime, timedelta
            start_time = datetime(2019, 5, 13, 19, 30, 0)
            print(type(start_time))
            end_time = start_time + timedelta(hours=4)
            timezone = 'Asia/Kolkata'
            event = {
            'summary': 'Mymedbook Appointment',
            'location': 'Bangalore',
            'description': 'Appointment with Dr. John',
            'start': {
                'dateTime': start_time.strftime("%Y-%m-%dT%H:%M:%S"),
                'timeZone': timezone,
            },
            'end': {
                'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S"),
                'timeZone': timezone,
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
            print(event['hangoutLink'])
            res =  {
                'message': 'Event created successfully',
                'status': status.HTTP_200_OK,
                'data': {
                    'event': event.get('summary'),
                    'hangout_url': event.get('hangoutLink'),
                    'start': event.get('start').get('dateTime'),
                    'end': event.get('end').get('dateTime'),
                    'event_link': event.get('htmlLink'),
                }

            }
            return res




    