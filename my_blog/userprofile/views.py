from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from .forms import UserLoginForm,UserRegisterForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from .models import Profile

def user_login(request):
    if request.method == 'POST':
        user_login_form = UserLoginForm(data=request.POST)
        if user_login_form.is_valid():
            # cleaned_data 清晰出合法数据
            data = user_login_form.cleaned_data
            user = authenticate(username=data['username'],password=data['password'])
            if user:
                login(request,user)
                return redirect("article:article_list")
            else:
                return HttpResponse("账号或密码输入有误,请重新输入")
        else:
            return HttpResponse("账号或密码输入不合法")
        
    elif request.method == 'GET':
        user_login_form = UserLoginForm()
        context = {'form':user_login_form}
        return render(request,'userprofile/login.html',context)
    else:
        return HttpResponse("请使用GET或POST请求数据")
    
def user_logout(request):
    logout(request)
    return redirect("article:article_list")

def user_register(request):
    if request.method == 'POST':
        user_register_form = UserRegisterForm(data=request.POST)
        if user_register_form.is_valid():
            new_user = user_register_form.save(commit=False)
            new_user.set_password(user_register_form.cleaned_data['password'])
            new_user.save()
            login(request,new_user)
            return redirect("article:article_list")
        else:
            return HttpResponse("注册表单输入有误,请重新输入")
    elif request.method == 'GET':
        user_register_form = UserRegisterForm()
        context = {'form':user_register_form}
        return render(request,'userprofile/register.html',context)
    else:
        return HttpResponse('请使用GET或post请求数据')
    
@login_required(login_url='/userprofile/login/')
def user_delete(request,id):
    user = User.objects.get(id=id)
    if request.method == 'POST':
        if request.user == user:
            logout(request)
            user.delete()
            return redirect("article:article_list")
        else:
            return HttpResponse("你没有删除操作的权限")
    else:
        return HttpResponse("近接受post请求")
    
@login_required(login_url='/userprofile/login')
def profile_edit(request,id):
    user = User.objects.get(id=id)

    if Profile.objects.filter(user_id=id).exists():
        profile = Profile.objects.get(user_id=id)
    else:
        profile = Profile.objects.get(user=user)

    profile_form = ProfileForm(request.POST,request.FILES)

    if profile_form.is_valid():
        if 'avatar' in request.FILES:
            profile.avater = profile_cd["avatar"]
    