import time
import redis
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
conn_r=redis.Redis(host='127.0.0.1',port=6379)

class RequestBlockingMiddleware(MiddlewareMixin):
    def process_request(self,request):
        global num
        ip_in = request.META.get('REMOTE_ADDR')
        if conn_r.get(ip_in):
            return HttpResponse('操作繁忙')
        else:
            conn_r.set(ip_in, 'num', ex=2)