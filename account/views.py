from django.shortcuts import render, redirect
from .froms import RegisterForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from codes.forms import CodeForm
from .models import CustomUser
from .utils import send_sms
# Create your views here.
def Home(request):
    return render(request, 'home.html')

def RegisterView(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    dict = {'form':form}
    return render(request, 'register.html', context=dict)

def LoginView(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                request.session['pk'] = user.pk
                return redirect('verify')
    dict = {'form': form}
    return render(request, 'login.html', context=dict) 

def VerifyCode(request):
    form = CodeForm(request.POST or None)
    pk = request.session.get('pk')
    if pk:
        user = CustomUser.objects.get(pk=pk)
        code = user.code
        phone_number = user.phone_number
        code_user = f"{user.username}: {user.code}"

        if not request.POST:
            send_sms(code_user, phone_number)
            # send sms
            print(code_user)
        if form.is_valid():
            num = form.cleaned_data.get('number')

            if str(code)==num:
                code.save()
                login(request, user)
                return redirect('home')
            else:
                return redirect('login')

    dict = {'form': form}
    return render(request, 'verify.html', context=dict)