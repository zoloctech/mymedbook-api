from users.models import TempData
from django.conf import settings
from django.core.mail import send_mail
import requests
import random


def send_phone_otp(phone):
    if phone:
        otp = random.randint(999, 9999)
        url = "https://www.fast2sms.com/dev/bulk"
        api = "we6075JbW2GRqtTNa8MFBj9ESYOLD1HXiKVxPCQZzucmopUghy90sh62wI7YeQjOn4t5HSJUdKEBXWyk"
        message = "Hello ! Mymedbook User your Verification OTP is " + str(otp)
        querystring = {"authorization": api, "sender_id": "MymedbookSMS", "variables_values": otp,
                       "message": message, "language": "english", "route": "p", "numbers": phone}
        headers = {
            'cache-control': "no-cache"
        }
        result = requests.request(
            "GET", url, headers=headers, params=querystring)
        return otp
    else:
        return None


def send_email_otp(email):
    if email:
        otp = random.randint(999, 9999)
        subject = 'Email Verification for Mymedbook !'
        message = f'Welcome to Mymedbook ! Hello you are requesting to Email Verification for this mail {email} and your email OTP is {otp} . Please use this OTP to verify your email.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email, ]
        send_mail( subject, message, email_from, recipient_list,fail_silently=False) 
        return otp
    else:
        return None

