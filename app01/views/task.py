from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from app01 import models
import json
from django import forms
from django.http import JsonResponse
from app01.utils.form import BootStrapModelForm
from app01.utils.pagination import Pagination


class TaskModelForm(BootStrapModelForm):
    class Meta:
        model=models.Task
        fields='__all__'
        widgets={
            'detail':forms.TextInput,
            #'detail':forms.Textarea,
        }
def task_list(request):
    form=TaskModelForm()
    queryset=models.Task.objects.all().order_by('-id')
    page_object=Pagination(request,queryset,page_size=3)
    context={
        'form':form,
        'queryset':page_object.page_queryset,
        'page_string':page_object.html()
    }
    return render(request,'task_list.html',context)

@csrf_exempt
def task_ajax(request):
    print(request.POST)
    data_dict={'status':True,'data':[11,22,33,44]}
    return HttpResponse(json.dumps(data_dict))

@csrf_exempt
def task_add(request):
    form=TaskModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        data_dict = {'status': True}
        return JsonResponse(data_dict)
    data_dict = {'status': False,'error':form.errors}
    return JsonResponse(data_dict)
