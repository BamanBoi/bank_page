import requests
import random
from django.conf import settings
from django.core.mail import send_mail
def send_otp_to_phone(phone_number):
    try:
        otp = random.randint(1000, 9999)
        url=f'https://2factor.in/API/V1/{settings.APIKEY}/SMS/{phone_number}/{otp}'
        response = requests.get(url)
        return otp
    except Exception as e:
        return None
def send_otp_to_email(email):
    subject="Your transaction email"
    otp = random.randint(1000,9999)
    message = f'Your otp is:{otp}'
    email_from = settings.EMAIL_HOST_USER
    send_mail(subject,message,email_from,[email])
    return otp
    