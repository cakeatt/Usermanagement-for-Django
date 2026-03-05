from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from app01 import models
import json
from django import forms
from django.http import JsonResponse
import random
from datetime import datetime
from app01.models import Order
from app01.utils.form import BootStrapModelForm
from app01.utils.pagination import Pagination



class OrderModelForm(BootStrapModelForm):
    class Meta:
        model = models.Order
        # fields="__all__"
        exclude=['oid','admin']
def order_list(request):
    queryset=models.Order.objects.all()
    page_object=Pagination(request,queryset,page_size=4)
    form = OrderModelForm()
    context={
        'queryset':page_object.page_queryset,
        'page_string':page_object.html(),
        'form':form,
    }

    return render(request,'order_list.html',context)

@csrf_exempt
def order_add(request):
    form=OrderModelForm(data=request.POST)
    if form.is_valid():
        form.instance.oid=datetime.now().strftime('%Y%m%d%H%M%S')+str(random.randint(1000,9999))
        form.instance.admin_id=request.session['info']['id']
        form.save()
        return JsonResponse({'status':True})
    return JsonResponse({'status':False,'error':form.errors})

def order_delete(request):
    """删除订单"""
    uid=request.GET.get('uid')
    models.Order.objects.filter(id=uid).delete()
    return JsonResponse({'status':True})

def order_detail(request):
    """获取订单详细"""
    uid=request.GET.get('uid')
    row_dict=models.Order.objects.filter(id=uid).values('title','price','status').first()
    result={
        'status':True,
        'data':row_dict,
    }
    return JsonResponse(result)

@csrf_exempt
def order_edit(request):
    """编辑订单"""
    uid=request.GET.get('uid')
    row_object=models.Order.objects.filter(id=uid).first()
    form=OrderModelForm(data=request.POST,instance=row_object)
    if form.is_valid():
        form.save()
        return JsonResponse({'status':True})
    return JsonResponse({'status': False, 'error': form.errors})