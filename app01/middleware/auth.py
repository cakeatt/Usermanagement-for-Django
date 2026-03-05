from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse, redirect


class M1(MiddlewareMixin):

    def process_request(self,request):
        # 如果方法中没有返回值,继续往后走
        # 如果有返回值,不再继续，
        if request.path_info in ['/login/','/img/code/']:
            return
        info_dict=request.session.get('info')
        if info_dict:
            return
        return redirect('http://127.0.0.1:8000/login/')

    def process_response(self,request,response):

        return response