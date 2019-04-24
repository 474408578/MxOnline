from django.contrib.auth.hashers import make_password
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from utlis.email_send import send_register_email
from django.views.generic.base import View
from django.contrib.auth.backends import ModelBackend
from .models import UserProfile, EmailVerifyRecord
from django.db.models import Q
from .forms import LoginForm, RegisterForm, ForgetPwdForm, ModifyPwdForm


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Q对象将查询条件组合起来，使用并集查询
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            # django的后台中密码加密：所以不能password==password
            # UserProfile继承的AbstractUser中有def check_password(self, raw_password):
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})
    
    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username = request.POST.get('email', None)
            if UserProfile.objects.filter(email=username):
                return render(request, 'register.html', {'register_form': register_form, 'msg': '用户已存在'})
            else:
                password = request.POST.get('password', None)
                # 实例化一个UserProfile对象
                user_profile = UserProfile()
                user_profile.username = username
                user_profile.email = username
                # is_active默认为True,修改为False,只有用户去邮箱激活之后才改为True
                user_profile.is_active = False
                # 对保存到数据库的密码加密
                user_profile.password = make_password(password)
                user_profile.save()
                # 注册成功发送邮件,username是邮箱，
                send_register_email(username, 'register')
                return render(request, 'login.html')
        else:
            return render(request, 'register.html', {'register_form': register_form})
            

# 激活用户
'''
逻辑：访问到视图的时候将其激活
'''
class ActiveUserView(View):
    # active_code是在urls.py中传过来的
    def get(self, request, active_code):
        records = EmailVerifyRecord.objects.filter(code=active_code)
        if records:
            for record in records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
                return render(request, 'login.html')
        else:
            return render(request, 'register.html', {'msg': '您的激活链接无效'})
    
        
        



# def user_login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username', None)
#         password = request.POST.get('password', None)
#
#         # 验证用户的证书
#         user = authenticate(username=username, password=password)
#         if user is not None:
#             # login接受一个 HttpRequest对象和一个User对象作为参数,
#             # 使用Django的会话（ session ）框架把用户的ID保存在该会话中
#             login(request, user)
#             return render(request, 'index.html')
#         else:
#             return render(request, 'login.html', {'msg': '用户名或密码错误'})
#
#     elif request.method == 'GET':
#         return render(request, 'login.html')


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')
    
    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST.get('username', None)
            password = request.POST.get('password', None)
            
            user = authenticate(username=username, password=password)
            
            if user is not None:
                if user.is_active == True:
                    login(request, user)
                    return render(request, 'index.html')
                else:
                    return render(request, 'login.html', {'msg': '用户未激活', 'login_form': login_form})
            else:
                msg = '用户名或密码错误'
                return render(request, 'login.html', {'msg': msg})
        
        else:
            return render(request, 'login.html', {'login_form': login_form})
        
        
class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetPwdForm()
        return render(request, 'forgetpwd.html', {'forget_form': forget_form})
    
    def post(self, request):
        forget_form = ForgetPwdForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email', None)
            if UserProfile.objects.filter(email=email):
                send_register_email(email, 'forget')
                return render(request, 'send_success.html')
            else:
                return render(request, 'forgetpwd.html', {'msg': '邮箱还未注册'})
        else:
            return render(request, 'forgetpwd.html', {'forget_form': forget_form})


class ResetView(View):
    def get(self, request, active_code):
        records = EmailVerifyRecord.objects.filter(code=active_code)
        if records:
            for record in records:
                email = record.email
                return render(request, 'reset_password.html', {'email': email})
        else:
            return render(request, 'active_fail.html')
    
    
class ModifyPwdView(View):
    def get(self, request):
        modify_form = ModifyPwdForm()
        render(request, 'reset_password.html', {'modify': modify_form})
        
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1', None)
            pwd2 = request.POST.get('password2', None)
            email = request.POST.get('email', None)
            
            if pwd1 != pwd2:
                return render(request, 'reset_password.html', {'email': email, 'msg': '密码不一致!'})
            
            else:
                user = UserProfile.objects.get(email=email)
                user.password = make_password(pwd1)
                user.save()
                
                return render(request, 'login.html')
        else:
            email = request.POST.get('email', None)
            return render(request, 'reset_password.html', {'email': email, 'modify_form': modify_form})