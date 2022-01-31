from cmd import IDENTCHARS
import re
from turtle import backward
from django.shortcuts import redirect, render
from django.contrib.auth.models import User as us
from django.http import HttpResponse
from django.contrib import messages
from datetime import datetime
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_process
from django.contrib.auth import logout as logout_process
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.core.exceptions import ObjectDoesNotExist
from .models import BookApointment,UserAddress,User,BookingCategories,Photographers,CurrentBookings,WebsiteForm,UserHistory
from django.contrib.auth.hashers import make_password
#Email settings
server=smtplib.SMTP('smtp.gmail.com:587')
server.ehlo()
server.starttls()
server.login('photographerywebsite@gmail.com','kvyiutzopbyjaiqe')   #password: django@123

login_user=[]
user_email=''
user_name=''

login_user_name=''


def fetch_book(name):
    bk=[]
    book=list(BookApointment.objects.all())
    for i in book:
        if i.user_booking_name==name:
            bk.append([i.id,i.user_booking_category,i.user_booking_photographer,i.user_booking_datetime,i.user_booking_name,i.user_booking_phone,i.user_booking_address])
    return bk

def home(request):
    if request.method=="POST":
        print("home")
        name=request.POST['name']
        email=request.POST['email']
        subject=request.POST['subject']
        message=request.POST['message']
        obj=WebsiteForm(your_name=name,your_email=email,subject=subject,message=message)
        obj.save()
        messages.info(request,'Thanks for your message')
        return redirect('/#contact')
    else:
        return render(request, 'index.html')


def order(request):
    global user_email,user_name
    if request.method=='POST':
        try:
            name=request.POST['name']
            photographer=request.POST.get('photographer')
            date=datetime.strptime(request.POST['date'], "%Y-%m-%dT%H:%M")
            address=request.POST['address']
            category=request.POST['category']
            phone=request.POST['phone']
            # print(name,description,date,address,category,phone)
            usr=BookApointment(user_booking_name=name,user_booking_phone=phone,user_booking_datetime=date,user_booking_photographer=photographer,user_booking_address=address,user_booking_category=category)
            usr.save()
            # user=User.objects.get(id=2)
            # print(user)
            # BookApointment.user_id=user
            # BookApointment.user_booking_address=address
            # BookApointment.user_booking_date=date
            # BookApointment.user_booking_description=description
            # BookApointment.user_booking_category=category
            # print(login_user_name)

            users=User.objects.get(user_first_name=login_user_name)
            # print(users.user_last_name)

            # Message to send in email:
            message = MIMEMultipart("alternative")
            message["Subject"] = "Booking confirmation: Thank you for booking an appointment with us!"


            # Create the plain-text and HTML version of your message
            text = """\
            Dear customer,
            Thank you for choosing Photographery!
            A customer representative agent will contact you shortly with more details about your booking."""
            html = """\
            <html>
            <body>
                <p>Dear customer<br>
                Thank you for choosing Photographery!<br>
                A customer representative agent will contact you shortly with more details about your booking.
                </p>
            </body>
            </html>
            """

            # Turn these into plain/html MIMEText objects
            part1 = MIMEText(text, "plain")
            part2 = MIMEText(html, "html")

            # Add HTML/plain-text parts to MIMEMultipart message
            # The email client will try to render the last part first
            message.attach(part1)
            message.attach(part2)

            # serv=ServiceDetails.objects.get(id=users.id)
            # email=users.user_email
            # print("^^^^^^^^^^^^^^^^^^^^^^^^",email,"***************************")
            server.sendmail('photographerywebsite@gmail.com',str(users.user_email), message.as_string())

            # serv=ServiceDetails.objects.get(id=users.id)
            serv=BookingCategories.objects.get(category_name=category)

            current=CurrentBookings(user=users,service=serv,fulfillment=False,has_paid=False)
            current.save()

            history=UserHistory(user=users,user_service=serv,fulfillment=False,order_date=date)
            history.save()
            # time=request.POST['time']
            # print(name,description,date)
            # print(type(date))
            # print(type(time))

            booking=BookingCategories.objects.all()
            ct=[]
            for i in booking:
                ct.append(i.category_name)
            print(ct)
            photo=Photographers.objects.all()
            ph=[]
            for i in photo:
                ph.append(i.photographer_first_name)
            print(ph)
            u=User.objects.get(user_email=user_email)
            his=UserAddress.objects.get(user=u)

            # for i in list(BookApointment.objects.all()).split(','):
            #     if i.user_booking_name==name:
            #         print(i.user_booking_name,i.user_booking_phone,i.user_booking_datetime,i.user_booking_photographer,i.user_booking_address,i.user_booking_category)
            # print(bk)
            return render(request,'order_details.html'
            ,{
            # 'booking':ct,
            # 'photographer':ph,
            'book':fetch_book(user_name),
            'loginuser':user_email,
            # "fname":u.user_first_name,
            # "lname":u.user_last_name,
            # "phone":his.user_house_number,
            # "address":his.user_street,
            # "city":his.user_city,
            # "country":his.user_country,
            # "code":his.user_zip_code
            }
            )
        except Exception as e:
            print('order exception occur')
            print(e)
    else:
        if user_name!="":
            u=User.objects.get(user_email=user_email)
            booking=BookingCategories.objects.all()
            ct=[]
            for i in booking:
                ct.append(i.category_name)
            # print(ct)
            photo=Photographers.objects.all()
            ph=[]
            for i in photo:
                ph.append(i.photographer_first_name)
            # print(ph)
            # his=UserAddress.objects.get(user=u)
            # bk=[]
            # book=list(BookApointment.objects.all())
            # for i in book:
            #     if i.user_booking_name==user_name:
            #         bk.append([i.user_booking_category,i.user_booking_photographer,i.user_booking_datetime,i.user_booking_name,i.user_booking_phone,i.user_booking_address])
            return render(request,'order.html',
            {'booking':ct,
            'photographer':ph,
            'loginuser':user_email,
            # 'book':bk,
            "fname":u.user_first_name,
            # "lname":u.user_last_name,
            # "phone":his.user_house_number,
            # "address":his.user_street,
            # "city":his.user_city,
            # "country":his.user_country,
            # "code":his.user_zip_code
            }
            )
        else:

            return render(request,'login.html')


def logout(request):
    global login_user,user_email,user_name
    lg=request.POST['logout']
    for i,j in enumerate(login_user):
        if lg in login_user[i]:
            login_user.pop(i)
    # logout_process(request)
    print("logout")
    print("logout users:",login_user)
    user_name,user_email='',''
    return redirect("/")

def order_details(request):
    global user_email,user_name,login_user
    if request.method=="POST":
        if request.POST.get('edit'):
            name=request.POST['name']
            id=request.POST['id']
            phone=request.POST['phone']
            address=request.POST['address']
            BookApointment.objects.filter(id=int(id)).update(user_booking_phone=phone,user_booking_address=address)
            return render(request,'order_details.html'
            ,{
            'book':fetch_book(user_name),
            'loginuser':user_email,
            }
            )

        else:
            # name=request.POST['edit']
            id=request.POST['id']
            BookApointment.objects.filter(id=int(id)).delete()

            return render(request,'order_details.html'
            ,{
            'book':fetch_book(user_name),
            'loginuser':user_email,
            }
            )

    else:
        try:
            return render(request,'order_details.html'
            ,{
            'book':fetch_book(user_name),
            'loginuser':user_email,
            }
            )
        except Exception as e:
            print(e)
            return render(request,'login.html')


def user_details(request):
    global user_email,user_name,login_user
    if request.method=="POST":
        fname=request.POST['fname']
        lname=request.POST['lname']
        phone=request.POST['phone']
        address=request.POST['address']
        city=request.POST['city']
        country=request.POST['country']
        code=request.POST['code']
        # print("post second error",e)
        uss=us.objects.get(email=user_email)
        uss.username=fname
        uss.first_name=fname
        uss.last_name=lname
        uss.save()
        u=User.objects.get(user_email=user_email)
        u.user_first_name=fname
        u.user_last_name=lname
        # u.user_phone=phone
        h=UserAddress.objects.get(user=u)
        h.user_house_number=phone
        h.user_street=address
        h.user_city=city
        h.user_country=country
        h.user_zip_code=code
        u.save()
        h.save()
        BookApointment.objects.filter(user_booking_name=user_name).update(user_booking_name=fname)
        user_name=fname
        u=User.objects.get(user_email=user_email)
        his=UserAddress.objects.get(user=u)
        return render(request,'user_details.html' ,{
        'loginuser':user_email,
        "fname":u.user_first_name,
        "lname":u.user_last_name,
        "phone":his.user_house_number,
        "address":his.user_street,
        "city":his.user_city,
        "country":his.user_country,
        "code":his.user_zip_code
        })
    else:
        try:
            u=User.objects.get(user_email=user_email)
            his=UserAddress.objects.get(user=u)
            return render(request,'user_details.html'
            ,{
            'loginuser':user_email,
            "fname":u.user_first_name,
            "lname":u.user_last_name,
            "phone":his.user_house_number,
            "address":his.user_street,
            "city":his.user_city,
            "country":his.user_country,
            "code":his.user_zip_code
            }
            )
        except Exception as e:
            print(e)
            return render(request,'login.html')

def login(request):
    global login_user_name
    global login_user
    global user_email
    global user_name
    if request.method=='POST':
        print("login")
        email=request.POST['email']
        password=request.POST['pass1']
        try:
            uk=us.objects.get(email=email)
            if uk.check_password(password):
                # login_process(request, user)
                if uk.is_superuser:
                    return redirect("/admin:index")
                print("login_process")
                login_user.append((email,password))
                print("login users",login_user)

                # print("password check",uk.check_password(password))
                u=User.objects.get(user_email=email)
                user_email=email
                user_name=u.user_first_name
                print("user_name",user_name)

                # print(user)
                login_user_name=uk.username
                uk=User.objects.get(user_first_name=user_name)
                login_user_name=uk.user_first_name
                print('###########################################')
                print(login_user_name)
                booking=BookingCategories.objects.all()
                ct=[]
                for i in booking:
                    ct.append(i.category_name)
                # print(ct)
                photo=Photographers.objects.all()
                ph=[]
                for i in photo:
                    ph.append(i.photographer_first_name)
                # print(ph)
                # his=UserAddress.objects.get(user=u)
                # bk=[]
                # book=list(BookApointment.objects.all())
                # for i in book:
                #     if i.user_booking_name==user_name:
                #         bk.append([i.user_booking_category,i.user_booking_photographer,i.user_booking_datetime,i.user_booking_name,i.user_booking_phone,i.user_booking_address])
                return render(request,'order.html',
                {'booking':ct,
                'photographer':ph,
                'loginuser':email,
                # 'book':bk,
                "fname":u.user_first_name,
                # "lname":u.user_last_name,
                # "phone":his.user_house_number,
                # "address":his.user_street,
                # "city":his.user_city,
                # "country":his.user_country,
                # "code":his.user_zip_code
                }
                )
                # No backend authenticated the credentials
            else:
                messages.error(request,'username or password not correct')
                # A backend authenticated the credentials
                return render(request,'login.html')
        except ObjectDoesNotExist as e:
            print("login :" ,e)
            messages.error(request,'username or password not correct')
            # A backend authenticated the credentials
            return render(request,'login.html')


    else:
        return render(request, 'login.html')

def signup(request):

    if request.method=='POST':
        print("sigup")
        fname=request.POST['fname']
        lname=request.POST['lname']
        phone=request.POST['phone']
        address=request.POST['address']
        city=request.POST['city']
        country=request.POST['country']
        pcode=request.POST['pcode']
        email=request.POST['email']
        password=request.POST['pass1']
        password1=request.POST['pass2']
        if password==password1:

            # if User.objects.filter(user_email=email).exists():
            if User.objects.filter(user_email=email).exists():

                messages.info(request,'email already exists')
                return redirect('/signup')
            r=us.objects.create_user(username=fname,email=email,password=password,first_name=fname,last_name=lname)
            user=User(user_first_name=fname,user_last_name=lname,user_email=email,user_password=make_password(password),is_super_user=False,user_account_name=fname+lname)
            # user.first_name=fname
            # user.last_name=lname

            u=UserAddress(user=user, user_house_number=phone,user_street=address,user_city=city,user_country=country,user_zip_code=pcode)

            # user.address=address
            # user.city=city
            # user.country=country
            # user.pcode=pcode
            user.save()
            u.save()
            r.save()
            return redirect('/login')
        else:
            messages.info(request,"password not match")
            return redirect('/signup')
        # print(fname,lname,phone,address,city,country,pcode,email,password,password1)
        # return redirect('/login')
    else:
        return render(request, 'signup.html')
