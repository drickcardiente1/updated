from django.shortcuts import render, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import logout, get_user_model, authenticate, login
from .forms import *
import requests
import json
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from .utils import *
import datetime


# Create your views here.

# social close form
def close(request):
    return render(request, 'partials/close.html')

# sign-out here.
def signout(request):
    logout(request)
    return redirect('login')

# home views here.
def home(request):
    if request.user.is_authenticated:
        id = request.user.id
        user = User.objects.get(id = id)
        context = {"user":user, "direction":"TE MOTORBIKES HOME"}
        return render(request, 'users/home.html', context)
    else:
        return render(request, 'users/home.html')

# sign-in here.
def log_in_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = LoginForm()
        form2 = Password_Reset_Confirm()
        return render(request, 'validation/login.html', {'form':form, 'form2':form2})

# sign-up proccess here.
def sign_up_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = RegistrationForm()
        return render(request, 'validation/register.html', {'form':form})
    
def profile_view(request):
    if request.user.is_authenticated:
        id = request.user.id
        user = User.objects.get(id = id)
        imgs = User_profile.objects.filter(created_by = request.user)
        context = {"user":user, "direction":"PROFILE", "imgs":imgs}
        return render(request, 'users/profile.html', context)
    else:
        return redirect('home')
    
def update_profile(request):
    if request.method == 'POST':
        try:
            uid = request.user.id
            user = User.objects.filter(id = uid)
            user.update(first_name = request.POST.get('first_name'), last_name = request.POST.get('last_name'), address = request.POST.get('address'), city = request.POST.get('city'), country = request.POST.get('country'), zipcode = request.POST.get('zipcode'), About_Me = request.POST.get('About_me'))
        except:
            return redirect('profile')
    return redirect('profile')

def update_profile_pic(request):
    img = User_profile.objects.create(created_by = request.user, profile_image=request.FILES.get('img'))
    User.objects.update(profile_image = img.profile_image)
    return redirect('profile')

# here
def update_profile_pic_from_saved(request):
    id = json.loads(request.POST.get('data'))
    to_set = User_profile.objects.get(id = id)
    User.objects.update(profile_image = to_set.profile_image)
    return redirect('profile')

# here
def save_profile_pic_from_take_picture(request):
    example = request.POST.get('data')
    img = b64toimg(example)
    uimg = User_profile.objects.create(created_by = request.user, profile_image=img)
    User.objects.update(profile_image = uimg.profile_image)
    return redirect('profile')
    
    

# sign-in proccess here.
def log_in_proccess(request):
    data = json.loads(request.POST.get('data'))
    response = requests.post('http://127.0.0.1:8000/api/login/', data)
    user = authenticate(username=data['username'], password=data['password'])
    if(response.status_code == 200):
        value = json.loads('{"success": "'+data['username']+'"}')
        login(request, user)
        return HttpResponse(json.dumps(value))
    else:
        return HttpResponse(response)
    
# forgot-password proccess here.
def forgot_password_proccess(request):
    data = json.load(request)['data']
    response = requests.post('http://127.0.0.1:8000/api/reset/sendotp/', data={'email': data})
    return HttpResponse(response)

# forgot-password proccess here.
def forgot_password_confirm_proccess(request):
    data = json.load(request)['TableData']
    response = requests.post('http://127.0.0.1:8000/api/reset/password/', data)
    requests.post('http://127.0.0.1:8000/api/login/', data = {"username":data['email'], "password":data['password']})
    user = authenticate(username=data['email'], password=data['password'])
    login(request, user)
    return HttpResponse(response)

# otp proccess here.
def action_otpsendregistration(request):
    data = json.loads(request.POST.get('data'))
    response = requests.post('http://127.0.0.1:8000/api/otp/', data={'email': data})
    if response.status_code == 201:
        return HttpResponse("success")
    else:
        return HttpResponse(response)
    
# sign-up proccess here.
def submit_register(request):
    data = json.loads(request.POST.get('data'))
    response = requests.post('http://127.0.0.1:8000/api/register/', data)
    if response.status_code == 201:
        return HttpResponse(response.status_code)
    else:
        return HttpResponse(response)
    
    
# home views here.
def user_stats(request):
    if request.user.is_anonymous:
        return HttpResponse(202)
    else:
        now = datetime.datetime.now()
        id = request.user.id
        user = User.objects.get(id = id)
        time = user.AuthTransaction.all().last()
        exp_time = time.expires_at
        exp = exp_time.astimezone()
        val = compare_dates(now, exp)
        if (not val):
            logout(request)
            return HttpResponse(101)
        return HttpResponse(205)
    