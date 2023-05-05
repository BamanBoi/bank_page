from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import authenticate,login
from django.contrib import messages
from .models import Credit
from .helpers import *
import base64
from PIL import Image
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
            #otp_e_= send_otp_to_email(email)
            return redirect('otpverify')
        else:
            messages.info(request,'Account not found')
            return redirect('creditcard')
    return render(request,'transaction/index.html')
def otp(request):
    if request.method=='POST':
        otp_rec=request.POST.get('m_otp')
        if(otp_!=0 and otp_==int(otp_rec)):
            return redirect('face')
        else:
            messages.info(request,'OTP incorrect')
            return redirect('creditcard')
    return render(request,'transaction/otp.html')
def face(request):
    if request.method=='POST':
        img = cards[ind].image
        img = open(str(img),'rb')
        known_image = face_recognition.load_image_file(img)
        cap_img=request.POST.get('captured_image_data')
        decoded_data=base64.b64decode(cap_img)
        img_file = open('temp.jpeg', 'wb')
        img_file.write(decoded_data)
        img_file.close()
        unknown_image = face_recognition.load_image_file('temp.jpeg')
        try:
            known_encoding = face_recognition.face_encodings(known_image)[0]
            unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
            results = face_recognition.compare_faces([known_encoding], unknown_encoding)
            if results[0]:
                img_file2= Image.open('white.jpeg')
                img_file = img_file2.save('temp.jpeg')
                return HttpResponse("Verification Successfull")
            else:
                img_file2= Image.open('white.jpeg')
                img_file = img_file2.save('temp.jpeg')
                messages.info(request,'Verification Unsuccessfull')
                return redirect('creditcard')
        except:
            messages.info(request,'Face Not Captured')
            return redirect('creditcard')
    return render(request,'transaction/face.html')
        