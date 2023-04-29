from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import authenticate,login
from .models import Credit
from .helpers import *
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
            return redirect('otpverify')
        else:
            print('Error')
    return render(request,'transaction/index.html')
def otp(request):
    if request.method=='POST':
        phone_number = cards[ind].mobile
        email = cards[ind].email
        #print(phone_number)
        otp_= send_otp_to_phone(phone_number)
        otp_e_= send_otp_to_email(email)
        #print(otp_)
        otp_rec=request.POST.get('m_otp')
        otp_rec_e=request.POST.get('e_otp')
        if(otp_==otp_rec and otp_e_==otp_rec_e):
            return HttpResponse("Verification successfull")
        else:
            return redirect('index.html')
    return render(request,'transaction/otp.html')