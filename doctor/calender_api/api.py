from asyncio import events
from pathlib import Path
from pickle import load
from pickle import dump
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from uuid import uuid4
from typing import Dict, List
import json

class EventPlanner:

    def __init__(self, guests: Dict[str, str], schedule: Dict[str, str]):
        guests = [{"email": email} for email in guests.values()]
        service = self._authorize()
        self.event_states = self._plan_event(guests, schedule, service)

    @staticmethod
    def _authorize():
        scopes = ["https://www.googleapis.com/auth/calendar"]
        credentials = None
        token_file = Path("token.pickle")

        if token_file.exists():
            with open(token_file, "rb") as token:
                credentials = load(token)

        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', scopes)
                credentials = flow.run_local_server(port=0)
            with open(token_file, "wb") as token:
                dump(credentials, token)

        calendar_service = build("calendar", "v3", credentials=credentials)

        return calendar_service

    @staticmethod
    def _plan_event(attendees: List[Dict[str, str]], event_time, service: build):
        event = {"summary": "Mymedbook meeting",
                 "start": {"dateTime": event_time["start"]},
                 "end": {"dateTime": event_time["end"]},
                 "attendees": attendees,
                 "conferenceData": {"createRequest": {"requestId": f"{uuid4().hex}",
                                                      "conferenceSolutionKey": {"type": "hangoutsMeet"}}},
                 "reminders": {"useDefault": True}
                 }
        print('ttttttt')
        event = service.events().insert(calendarId="primary", sendNotifications=True,
                                        body=event, conferenceDataVersion=1).execute()
        
        return event

    

if __name__ == "__main__":
    plan = EventPlanner({"test_guest": "pzoloctech@gmail.com"},
                        {"start": "2021-07-01T00:00:00.000+09:00", "end": "2022-07-01T00:30:00.000+09:00"})
    
