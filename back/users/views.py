from django.shortcuts import render,redirect,HttpResponse
from django.urls import reverse
import requests
from .models import CustomUser
from .forms import UserLogin,UserCreate
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout


class AuthView:

    def reg(request):
        if request.method == 'POST':
            form = UserCreate(request.POST)
            if form.is_valid():
                
                data = form.cleaned_data
                reg_url = request.build_absolute_uri(('/auth/users/'))
                response = requests.post(reg_url,json=data)
                if response.status_code == 201:
                    HttpResponse('User created\nPlease login')
                    return redirect('postlist')
                else:
                    # Обработайте ошибку API, например, передайте сообщение об ошибке в контекст
                    error_message = "Ошибка при регистрации: " + response.text
                    return render(request, 'main/reg.html', {'form': form, 'error': error_message})
        else:
            form = UserCreate()
            return render(request,'main/reg.html',{'form':form})
        

    
    def login(request):
        if request.method == 'POST':
            form = UserLogin(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                data = {'email':email, 'password':password}

                url = request.build_absolute_uri('/auth/token/login/')
                response = requests.post(url, json=data)

                user = authenticate(request, email=email, password=password)
                if user:
                    login(request, user)
                    
                if response.status_code == 200:
                    return redirect('postlist')
                else:
                    error = response.text
                    # Используем render для отображения страницы с формой и сообщением об ошибке
                    return render(request, 'main/login.html', {'form': form, 'error': error})
        else:
            form = UserLogin()
        return render(request, 'main/login.html', {'form': form})
    
    def logout(request):
        if request.user.is_authenticated:
            url = request.build_absolute_uri('/auth/token/logout/')
            user = request.user
            token, created = Token.objects.get_or_create(user=user)
            print(token.key)
            headers = {
                'Authorization':'Token '+ token.key
            }
            response = requests.post(url,headers=headers)
            if response.status_code == 204:
                logout(request)
                return redirect('postlist')
            else:
                error = response.text
                return HttpResponse(response.text)
        else:
            return HttpResponse('You are not logged in')
            
