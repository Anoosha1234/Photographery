from django.shortcuts import redirect, render
from django.contrib.auth.models import User as us
from django.http import HttpResponse
from django.contrib import messages
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

#creating views here


server=smtplib.SMTP('smtp.gmail.com:587')
server.ehlo()
server.starttls()
server.login('photographerywebsite@gmail.com','kvyiutzopbyjaiqe')   #password: django@123

from .models import BookApointment,UserAddress,User,BookingCategories,Photographers,CurrentBookings,WebsiteForm,UserHistory
from django.contrib.auth import authenticate
login_user_name=''
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
        return redirect('/')
    return render(request, 'index.html')


def order(request):
    if request.method=='POST':
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
        server.sendmail('djangoproject0347@gmail.com',str(users.user_email), message.as_string())

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
        return redirect('/')

    else:
        return render(request,'login.html')

def login(request):
    global login_user_name
    if request.method=='POST':
        print("login")
        email=request.POST['email']
        password=request.POST['pass1']
        user = authenticate(email=email, password=password)
        if user is not None:
            # A backend authenticated the credentials
            messages.info("invalid credentials ")
            return redirect(request,'/login')
        else:
            uk=us.objects.get(email=email)
            # u=user.objects.get(user_email=email)
            print(user)
            login_user_name=uk.username
            uk=User.objects.get(user_first_name=login_user_name)
            login_user_name=uk.user_first_name
            print('###########################################33')
            print(login_user_name)
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
            return render(request,'order.html',{'booking':ct,'photographer':ph})
            # No backend authenticated the credentials
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
            user=User(user_first_name=fname,user_last_name=lname,user_email=email,user_password=password,is_super_user=False,user_account_name=fname+lname)
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
