from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *

import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class NewContactDetail(APIView):
    def post(self, request):

        serializer = ContactDetailSerializer(data=request.POST)
        if serializer.is_valid():
            serializer.save()
            send_email_function(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NewRegistration(APIView):
    def post(self, request):
        serializer = ELANRegistrationSerializer(data=request.POST)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def send_email_function(data):
    EMAILS = {
        'PR': 'krati@elan.org.in',
        'Sponsorship': 'ashutosh.t@elan.org.in',
        'Shows': 'adyasa.m@elan.org.in',
        'Workshop': 'mahesh.s@elan.org.in',
        'Culti': 'sharanya@elan.org.in',       # Change Later!!!
        'Biggies': 'sharanya@elan.org.in',
        'Techy': 'mahesh.s@elan.org.in',
        'Social Cause': 'sharanya@elan.org.in',
        'Informals': 'krati@elan.org.in',
        'Miscellaneous': 'info@elan.org.in',
        'Finance': 'finance.head@elan.org.in',
        'Merch': 'finance.head@elan.org.in'
    }

    PORT = 465
    SMTP_SERVER = "smtp.gmail.com"
    SENDER_EMAIL = "info@elan.org.in"
    receiver_email = EMAILS[data['domain']]
    PASSWORD = "info#elan"


    message = MIMEMultipart("alternative")
    message["Subject"] = f"{data['domain']} Query"
    message["From"] = SENDER_EMAIL
    message["To"] = receiver_email

    text = f"""\
    {data['message']}
    
    Contact Details:
    Name: {data['name']}
    Email: {data['email']}
    Phone: {data['phone']}"""

    html = f"""\
    <html>
      <body>
        <p>
            {data['message']}
        </p>
        <h4>Contact Details:</h4>
        <div>Name: {data['name']}</div>
        <div>Email: {data['email']}</div>
        <div>Phone: {data['phone']}</div>
      </body>
    </html>
    """

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    message.attach(part1)
    message.attach(part2)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(SMTP_SERVER, PORT, context=context) as server:
        server.login(SENDER_EMAIL, PASSWORD)
        server.sendmail(SENDER_EMAIL, receiver_email, message.as_string())
