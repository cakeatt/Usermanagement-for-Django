from django.forms.widgets import TextInput
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django import forms

from app01 import models
from app01.utils.form import BootStrapForm
from app01.utils.encrypt import md5
from app01.utils.code import check_code
from io import BytesIO

class LoginForm(BootStrapForm):
    username=forms.CharField(label='用户名',widget=forms.TextInput,required=True)
    password=forms.CharField(label='密码',widget=forms.PasswordInput(render_value=True),required=True)
    code=forms.CharField(label='验证码',widget=TextInput,required=True)
    def clean_password(self):
        return md5(self.cleaned_data.get('password'))

def login(request):
    if request.method == 'GET':
        form=LoginForm()
        return render(request,'login.html', {'form':form})
    form =LoginForm(data=request.POST)
    if form.is_valid():
        user_input_code=form.cleaned_data.pop('code')
        img_code=request.session.get('img_code','')
        if user_input_code.lower() != img_code.lower():
            form.add_error('code','验证码错误')
            return render(request,'login.html', {'form':form})

        admin_object=models.Admin.objects.filter(**form.cleaned_data).first()
        if not admin_object:
            form.add_error('password','用户名或密码错误')
            return render(request, 'login.html', {'form': form})
        request.session['info']= {'id':admin_object.id,'username':admin_object.username}
        request.session.set_expiry(60*60*24*7)
        return redirect('http://127.0.0.1:8000/admin/list/')
    return render(request,'login.html', {'form':form})

def logout(request):
    request.session.clear()
    return redirect('http://127.0.0.1:8000/login/')

def img_code(request):
    img,code_string=check_code()
    request.session['img_code'] = code_string
    request.session.set_expiry(60) #60秒超时
    stream=BytesIO()
    img.save(stream,'png')
    stream.getvalue()
    return HttpResponse(stream.getvalue())