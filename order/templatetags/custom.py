from django import template
from django.template.defaultfilters import stringfilter
from ertong.order.models import PlayProject,Perform,Order,ProjectType,Ticket

register = template.Library()

@stringfilter
@register.filter
def truncateletters(value, num):
    try:
        num = int(num)
        if len(value) > num:
            value = "%s..." % value[:num-1]
    except:
        value = ''
    return value
    

@stringfilter
@register.filter
def get_ticket(value):
    print "1122"
    ticket = Ticket.objects.filter(perform=value)
    print "is ticket",ticket[0].price
    return ticket
