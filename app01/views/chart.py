from django.forms.widgets import TextInput
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django import forms
from app01 import models
from django.http import JsonResponse

def chart_list(request):
    """数据统计页面"""
    return render(request,'chart_list.html')

def chart_bar(request):
    """构造柱状图数据"""
    legend=['mikasa','chisa']

    series_list=[
        {
            'name': 'mikasa',
            'type': 'bar',
            'data': [5, 20, 36, 10, 10, 20]
        },
        {
            'name': 'chisa',
            'type': 'bar',
            'data': [20, 16, 26, 20, 28, 29]
        }
    ]

    x_xis=['一月', '二月', '三月', '四月', '五月', '七月']

    result={
        'status': True,
        'data': {
            'legend': legend,
            'series_list': series_list,
            'x_xis': x_xis,
        }
    }

    return JsonResponse(result)