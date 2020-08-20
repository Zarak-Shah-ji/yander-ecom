from django import template
from core.models import Order

#this is used so that we can register our template tag
register = template.Library()

#define a func that has the name of the template tag
@register.filter
#it counts the number of different items in your cart
def cart_item_count(user):
    if user.is_authenticated:
        #qs means query set
        #ordered is kept false bcoz we don't want to get the users previously ordered items
        qs = Order.objects.filter(user=user,ordered=False)
        if qs.exists():
            #returning the only order if it exists and keeping the count of it 
            return qs[0].items.count()
    #if user is not authenticated
    return 0
