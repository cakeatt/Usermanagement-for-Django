from django.db.models import CharField
from django.shortcuts import render,redirect
from app01 import models
from app01.utils.pagination import Pagination
from app01.utils.form import UserModelForm
# Create your views here.

def user_list(request):

    queryset=models.UserInfo.objects.all()
    page_object=Pagination(request,queryset,page_size=2)
    context={
        'queryset':page_object.page_queryset,
        'page_string':page_object.html()
    }
    return render(request,'user_list.html',context)

def user_add(request):
    if request.method=='GET':
        form=UserModelForm()
        return render(request,'user_add.html',{"form":form})
    form=UserModelForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('http://127.0.0.1:8000/user/list/')
    return render(request,'user_add.html',{"form":form})

def user_edit(request,nid):
    row_object = models.UserInfo.objects.filter(id=nid).first()
    if request.method=='GET':
        form=UserModelForm(instance=row_object)
        return render(request,'user_edit.html',{"form":form})
    form=UserModelForm(data=request.POST,instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('http://127.0.0.1:8000/user/list/')
    return render(request,'user_edit.html',{"form":form})

def user_delete(request,nid):
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect('http://127.0.0.1:8000/user/list/')
