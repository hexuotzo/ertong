# -*- coding:utf-8 -*-
from django.contrib import admin
from ertong.order.models import PlayProject,Order,Perform
class PlayAdmin(admin.ModelAdmin):
    list_filter = ('area','type')
    list_display = ('name','type','pay','area','begin_time','end_time')
    search_fields = ['name','area']

def register(modeladmin, request, queryset):
    queryset.update(register=True)
register.short_description = u"激活"

def unregister(modeladmin, request, queryset):
    queryset.update(register=False)
unregister.short_description = u"取消激活"

class PerAdmin(admin.ModelAdmin):
    list_filter = ('project','register')
    list_display = ('project','area','pay','play_time','register')
    search_fields = ['play_time',]
    actions = [register,unregister]


class OrderAdmin(admin.ModelAdmin):
    list_filter = ('order_time','changci')
    list_display = ('order_id','changci','order_time','pay','user','phonenum')
    search_fields = ['order_id','user','phonenum']




admin.site.register(Perform,PerAdmin)
admin.site.register(PlayProject,PlayAdmin)
admin.site.register(Order,OrderAdmin)
