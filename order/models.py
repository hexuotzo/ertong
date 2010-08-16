# -*- coding:utf-8 -*-
from django.db import models
import datetime
# Create your models here.
def decode(info):
    return info.decode('UTF-8')

STATUS_CHOICES = (('0','<font color=blue>[预定中]</font>'),
                  ('1','<font color=red>[售票中]</font>'),
                 )
    

class Area(models.Model):
    '''
    地区
    '''
    name = models.CharField(max_length=200,verbose_name="*名称")
    class Meta:
        verbose_name= decode("地区")
        verbose_name_plural = decode("地区管理")
    def __unicode__(self):
        return self.name

class Venues(models.Model):
    '''
    场馆
    '''
    name = models.CharField(max_length=200,verbose_name="*场馆名称")
    #pic = models.ImageField(upload_to = 'venues_pic',help_text='请使用 .jpg 格式的图片',verbose_name='*图片' )
    area = models.ForeignKey(Area,verbose_name="*地点")
    info = models.TextField(verbose_name="介绍")
    address = models.CharField(max_length=400,verbose_name="*地址")
    line = models.TextField(verbose_name="乘车路线")
    class Meta:
        verbose_name= decode("场馆")
        verbose_name_plural = decode("场馆管理")
    def __unicode__(self):
        return self.name
class ProjectType(models.Model):
    '''
    项目类型
    '''
    name = models.CharField(max_length=200,verbose_name="*类型",help_text="例：儿童剧，木偶剧等等")
    class Meta:
        verbose_name= decode("项目类型")
        verbose_name_plural = decode("项目类型管理")
    def __unicode__(self):
        return self.name


class PlayProject(models.Model):
    '''
    演出项目
    '''
    name = models.CharField(max_length=200,verbose_name="*项目名称",unique=True)
    type = models.ForeignKey(ProjectType,verbose_name="*项目类型")
    status = models.CharField(max_length=1,choices=STATUS_CHOICES)
    #pic = models.ImageField(upload_to = 'project_pic',help_text='请使用 .jpg 格式的图片',verbose_name='*项目图片' )
    #top_pic = models.ImageField(upload_to = 'top_pic',help_text='请使用 .jpg 格式的图片(可为空)',blank=True,verbose_name='热点图片')
    info = models.TextField(verbose_name="介绍")
    pay = models.CharField(max_length=200,verbose_name="*价格",help_text="多种价格以'/'分隔，例：100/200/300/350")
    venues = models.ForeignKey(Venues,verbose_name="*场馆")
    begin_time = models.DateField(auto_now=False,auto_now_add=False,verbose_name="*开始时间")
    end_time = models.DateField(auto_now=False,auto_now_add=False,verbose_name="*结束时间")
    show_time = models.CharField(max_length=200,verbose_name="*演出时间",help_text="填写具体时间，例：上午10:00-上午11:30")
    register = models.BooleanField(verbose_name="激活")
    class Meta:
        verbose_name = decode("项目表")
        verbose_name_plural = decode("项目管理")
    def __unicode__(self):
        return self.name
    def save(self):
        create = True if self.id else False
        super(PlayProject, self).save()
        if not create:
            time = self.end_time-self.begin_time
            for day in range(time.days+1):
                s_time = self.begin_time + datetime.timedelta(days=day)
                p = Perform(project_id=self.id,play_time=s_time,register=False)
                p.save()
                for i in self.pay.split("/"):
                    t = Ticket(perform=p,price=i,sold_out=False)
                    t.save()
    
class Perform(models.Model):
    '''
    场次管理
    '''
    project = models.ForeignKey(PlayProject,verbose_name="*项目")
    play_time = models.DateField(auto_now=False,auto_now_add=False,verbose_name="*演出日期")
    register = models.BooleanField(verbose_name="激活")
    class Meta:
        verbose_name = decode("场次表")
        verbose_name_plural = decode("场次管理")
    def __unicode__(self):
        return "%s__%s"%(self.project.name,self.play_time)

class Order(models.Model):
    '''
    订单表
    '''
    order_id = models.CharField('订单ID',max_length=11,blank=True,help_text="自动生成，编辑无效")
    discount = models.CharField(max_length=10,default="10",verbose_name="折扣")
    pay = models.FloatField(verbose_name="价格")
    order_time = models.DateTimeField(editable=False,auto_now=True,auto_now_add=False,verbose_name = "订单时间",help_text="系统记录不可修改")
    number = models.IntegerField(verbose_name="数量")
    changci = models.ForeignKey('Perform',verbose_name="对应场次")
    user = models.CharField(max_length=100,verbose_name="用户姓名")
    phonenum = models.CharField(max_length=12,verbose_name="用户手机号")
    user_area = models.CharField(max_length=300,verbose_name="送货地址")
    sum_pay = models.CharField(max_length=15,blank=True,verbose_name="总金额")
    def save(self):
        self.sum_pay = str(self.pay * self.number)
        super(Order, self).save()
        self.order_id = str(self.id + 100000000)
        super(Order, self).save()
    class Meta:
        verbose_name = decode("订单表")
        verbose_name_plural = decode("订单管理")
    def __unicode__(self):
        return self.order_id
    

class Ticket(models.Model):
    '''
    票价
    '''
    perform = models.ForeignKey(Perform)
    price = models.CharField("票价",max_length=15)
    sold_out = models.BooleanField("已售完")
    class Meta:
        verbose_name = decode("价格")
        verbose_name_plural = decode("票价")
        ordering = ('price',)
    def __unicode__(self):
        return self.price
