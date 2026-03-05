from django.db.models import CharField
from django.shortcuts import render,redirect
from app01 import models
from app01.utils.pagination import Pagination
from app01.utils.form import NumModelForm
# Create your views here.


def num_list(request):

    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["mobile__contains"] = search_data

    queryset = models.PrettyNum.objects.filter(**data_dict).order_by("-level")

    page_object = Pagination(request, queryset)

    context = {
        "search_data": search_data,

        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 页码
    }
    return render(request, 'num_list.html', context)

def num_add(request):
    if request.method=='GET':
        form=NumModelForm()
        return render(request,'num_add.html',{'form':form})
    form=NumModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('http://127.0.0.1:8000/num/list/')
    return render(request,'num_add.html',{'form':form})

def num_edit(request,nid):
    row_object=models.PrettyNum.objects.filter(id=nid).first()
    if request.method=='GET':
        form=NumModelForm(instance=row_object)
        return render(request,'num_edit.html',{'form':form})
    form=NumModelForm(data=request.POST,instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('http://127.0.0.1:8000/num/list/')
    return render(request,'num_edit.html',{'form':form})

def num_delete(request,nid):
    row_object=models.PrettyNum.objects.filter(id=nid).delete()
    return redirect('http://127.0.0.1:8000/num/list/')