# -*- coding:utf-8 -*-
from django.contrib import admin
from django import forms
from ertong.order.models import ProjectType,Venues,PlayProject,Order,Perform,Ticket,Area

def register(modeladmin, request, queryset):
    queryset.update(register=True)
register.short_description = u"激活"

def unregister(modeladmin, request, queryset):
    queryset.update(register=False)
unregister.short_description = u"取消激活"

def bookof(modeladmin, request, queryset):
    queryset.update(status="0")
bookof.short_description = u"预定中"

def ticketin(modeladmin, request, queryset):
    queryset.update(status="1")
ticketin.short_description = u"售票中"

class CustomForm(forms.ModelForm):
    class Meta:
        model = PlayProject 
    def clean_end_time(self):
        if self.data['begin_time']>self.data['end_time']:
            raise forms.ValidationError('结束时间早于开始时间')
        return self.cleaned_data["end_time"]

class PlayAdmin(admin.ModelAdmin):
    form = CustomForm
    list_filter = ('type','venues','status','register')
    list_display = ('name','type','status','pay','venues','begin_time','end_time','register')
    search_fields = ['name','venues']
    actions = [register,unregister,bookof,ticketin]
    

class TicketInline(admin.StackedInline):
    fieldsets = (
        (None, {
            'fields': (('price', 'sold_out'),)
        }),
    )
    model = Ticket
    extra = 20
    max_num = 20

class PerAdmin(admin.ModelAdmin):
    inlines = [TicketInline]
    list_display = ('project','play_time','register')
    list_filter = ('register','play_time','project')
    search_fields = ['play_time','area']
    actions = [register,unregister]


class OrderAdmin(admin.ModelAdmin):
    list_filter = ('order_time','changci')
    list_display = ('order_id','changci','order_time','user','phonenum','pay','number','sum_pay')
    search_fields = ['order_id','user','phonenum']


admin.site.register(Venues)
admin.site.register(Area)
admin.site.register(Perform,PerAdmin)
admin.site.register(PlayProject,PlayAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(ProjectType)
