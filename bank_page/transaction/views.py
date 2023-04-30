from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import authenticate,login
from .models import Credit
from .helpers import *
import base64
import face_recognition
# Create your views here.
cards=Credit.objects.all()
ind=0
def index(request):
    if request.method=='POST':
        size=len(cards)    
        number=request.POST.get('number')
        name=request.POST.get('holder_name')
        cvc=request.POST.get('cvc')
        month=request.POST.get('month')
        year=request.POST.get('year')
        flag=False
        for i in range(size):
            if(cards[i].Card_num==number and cards[i].holder_name==name and cards[i].cvv==cvc and cards[i].valid_month==month and cards[i].valid_year==year):
                ind=i
                flag=True
        if flag:
            phone_number = cards[ind].mobile
            email = cards[ind].email
            global otp_
            otp_=send_otp_to_phone(phone_number)
            global otp_e_
            otp_e_= send_otp_to_email(email)
            return redirect('otpverify')
        else:
            print('Error')
    return render(request,'transaction/index.html')
def otp(request):
    if request.method=='POST':
        otp_rec=request.POST.get('m_otp')
        otp_rec_e=request.POST.get('e_otp')
        if(otp_==otp_rec and otp_e_==otp_rec_e):
            return redirect('face')
        else:
            return redirect('index')
    return render(request,'transaction/otp.html')
def face(request):
    if request.method=='POST':
        img = cards[ind].image
        known_image = face_recognition.load_image_file(img)
        cap_img=request.POST.get('captured_image_data')
        decoded_data=base64.b64decode((cap_img))
        img_file = open('temp.jpeg', 'wb')
        img_file.write(decoded_data)
        unknown_image = face_recognition.load_image_file(img_file)
        known_encoding = face_recognition.face_encodings(known_image)[0]
        unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
        results = face_recognition.compare_faces([known_encoding], unknown_encoding)
    return render(request,'transaction/face.html')
        