from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from .models import Userdata,Doctorinfo,Appointmentinfo
from django.contrib import messages

def index(request):
    return render(request,'index.html')


def signup(request,method=['GET','POST']):
    if request.method=="POST":
        email=request.POST.get('email')
        password1=request.POST.get('password1')
        password2=request.POST.get('password2')
        user=Userdata.objects.filter(email=email)
        if user.exists:
            messages.info(request,"user already exists")
        elif password1 !=password2:
            messages.info(request,"password is not matched")
        else:
            messages.info(request,"user already exists")
            Userdata.objects.create(email=email,password=password1)
        return render(request,'main.html')
    return render(request,'signup.html')


def login(request,method=['GET','POST']):
    if request.method=="POST":
        email=request.POST.get('email')
        password1=request.POST.get('password1')
        
        user=Userdata.objects.filter(email=email,password=password1)
        if user.exists():
            request.session['email']=email
            return redirect('/main/')
        else:
            messages.info(request,'email and password is incorrect')
            return render(request,'login.html')
    
    return render(request,'login.html')

def main(request):
    email = request.session['email']
    doctors = Doctorinfo.objects.all()
    return render(request,'main.html',{'doctors':doctors,'email':email})

def appointment(request):

    if request.method=="POST":
        email = request.session['email']
        user=Userdata.objects.get(email=email)
        doctor = request.POST.get('doctor')
        doctorobj = Doctorinfo.objects.get(doc_name=doctor)
        patient = request.POST.get('patient')
        email_address = request.POST.get('email')
        contact = request.POST.get('contact')
        date_time = request.POST.get('date_time')
        symptoms = request.POST.get('symptoms')
        Appointmentinfo.objects.create(
            user=user, 
            doctor=doctorobj,
            patient_name = patient,
            email=email_address,
            contact=contact,
            date_time = date_time,
            symptoms=symptoms
        )
        return render(request,'success.html')
    return render(request,'appointment.html')


def book(request):
    return render(request, 'book.html')

# ---------------------- LOGOUT VIEW ----------------------
def logout(request):
    request.session.flush()  # Clear session
    messages.success(request, "Logged out successfully.")
    return redirect('/login/')

# Create your views here.
def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        # Use Django's authenticate (if using default User model)
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")  # Change "home" to your actual homepage URL name
        else:
            messages.error(request, "Email and password is incorrect")
    
    return render(request, "login.html")
