# -*- coding:utf-8 -*-
from django.db import models
import datetime
# Create your models here.
def decode(info):
    return info.decode('UTF-8')

TYPE_CHOICES = (('0','童话剧'),
                ('1','人偶剧'),
                ('2','木偶剧'),)

class PlayProject(models.Model):
    '''
    演出项目
    '''
    name = models.CharField(max_length=200,verbose_name="项目名称",unique=True)
    type = models.CharField(max_length=1,choices=TYPE_CHOICES)
    info = models.TextField(verbose_name="介绍")
    pay = models.CharField(max_length=200,verbose_name="价格",help_text="多种价格以'/'分隔，例：100/200/300/350")
    area = models.CharField(max_length=100,verbose_name="地点")
    begin_time = models.DateField(auto_now=False,auto_now_add=False,verbose_name="开始时间")
    end_time = models.DateField(auto_now=False,auto_now_add=False,verbose_name="结束时间")
    show_time = models.CharField(max_length=200,verbose_name="演出时间",help_text="填写具体时间，例：上午10:00-上午11:30")
    class Meta:
        verbose_name = decode("项目表")
        verbose_name_plural = decode("项目管理")
    def __unicode__(self):
        return self.name
    def save(self):
        super(PlayProject, self).save()   
        time = self.end_time-self.begin_time
        for i in range(time.days+1):
            s_time = self.begin_time + datetime.timedelta(days=i)
            p = Perform(project=self,pay=self.pay,area=self.area,play_time=s_time,show_time=self.show_time,register=False)
            p.save()     
    

class Perform(models.Model):
    '''
    场次管理
    '''
    project = models.ForeignKey('PlayProject',verbose_name="项目")
    pay = models.CharField(max_length=200,verbose_name="价格",help_text="多种价格以'/'分隔，例：100/200/300/350")
    area = models.CharField(max_length=100,verbose_name="地点")
    play_time = models.CharField(max_length=200,verbose_name="演出日期")
    show_time = models.CharField(max_length=200,verbose_name="演出时间",help_text="填写具体时间，例：上午10:00-上午11:30")
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
    order_id = models.CharField('订单ID',max_length=11,blank=True,help_text='ID为自动生成，自己写无效')
    discount = models.CharField(max_length=10,default="10",verbose_name="折扣")
    pay = models.FloatField(verbose_name="价格")
    order_time = models.DateTimeField(editable=False,auto_now=True,auto_now_add=False,verbose_name = "订单时间",help_text="系统记录不可修改")
    number = models.IntegerField(verbose_name="数量")
    changci = models.ForeignKey('Perform',verbose_name="对应场次")
    user = models.CharField(max_length=100,verbose_name="用户姓名")
    phonenum = models.CharField(max_length=12,verbose_name="用户手机号")
    user_area = models.CharField(max_length=300,verbose_name="送货地址")
    def save(self):
        super(Order, self).save()
        self.order_id = str(self.id + 100000000)
        super(Order, self).save()
    class Meta:
        verbose_name = decode("订单表")
        verbose_name_plural = decode("订单管理")
    def __unicode__(self):
        return self.order_id
    
    
