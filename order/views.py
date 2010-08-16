# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response
from ertong.order.models import PlayProject,Perform,Order,ProjectType,Ticket
import datetime
def index(request):
    return render_to_response("index.html")
    
    
def project(request):
    today = datetime.date.today()
    project = PlayProject.objects.filter(register=True,end_time__gte=today).order_by('type','begin_time')
    return render_to_response("project.html",locals())
    
def to_project(request,pid):
    today = datetime.date.today()
    project = PlayProject.objects.get(id=pid,end_time__gte=today,register=True)
    perform = Perform.objects.filter(project=project,register=True)
    return render_to_response("to_project.html",locals())
    
    
def get_order(request):
    if request.method == 'POST': 
        form = request.POST.copy()
        name = form.get("name")
        p = form.get("perform")
        perform = Perform.objects.get(id=p)
        pay = int(p.strip())
        phonenum = form.get("phonenum")
        number = int(form.get("number"))
        area = form.get("user_area")
        Order(user=name,changci=perform,pay=pay,phonenum=phonenum,number=number,user_area=area).save()
        return HttpResponse("完成,去<a href='/admin/order/order/'>后台</a>看看添加上了没？")
    raise Http404
