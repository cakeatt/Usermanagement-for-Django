from django.shortcuts import render,redirect
from app01 import models
from app01.utils.pagination import Pagination
from app01.utils.form import AdminModelForm,AdminResetModelForm

def admin_list(request):
    data_dict={}
    search_data=request.GET.get('q','')
    if search_data:
        data_dict['username__contains']=search_data
    queryset=models.Admin.objects.filter(**data_dict)
    page_object=Pagination(request,queryset,page_size=2)
    context={
        'queryset':page_object.page_queryset,
        'page_string':page_object.html(),
        'search_data':search_data,
    }
    return render(request,'admin_list.html',context)

def admin_add(request):

    if request.method=='GET':
        form=AdminModelForm()
        context={
            'form':form,
        }
        return render(request,'admin_add.html',context)
    form=AdminModelForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('http://127.0.0.1:8000/user/list/')
    context={
        'form':form,
    }
    return render(request,'admin_add.html',context)

def admin_edit(request,nid):
    row_object=models.Admin.objects.filter(id=nid).first()
    if request.method=='GET':
        if not row_object:
            return redirect('http://127.0.0.1:8000/admin/list/')
        form=AdminModelForm(instance=row_object)
        return render(request,'admin_edit.html',{'form':form})
    form=AdminModelForm(data=request.POST,instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('http://127.0.0.1:8000/admin/list/')
    return render(request,'admin_edit.html',)

def admin_reset(request,nid):
    row_object = models.Admin.objects.filter(id=nid).first()
    if request.method == 'GET':
        if not row_object:
            return redirect('http://127.0.0.1:8000/admin/list/')
        form=AdminResetModelForm(instance=row_object)
        return render(request,'admin_reset.html',{'form':form})
    form=AdminResetModelForm(data=request.POST,instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('http://127.0.0.1:8000/admin/list/')
    return render(request, 'admin_edit.html',{'form':form})
