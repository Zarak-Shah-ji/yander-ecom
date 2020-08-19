from django.conf import settings
from django.shortcuts import render ,get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
#importing our models to use their field in the context
from .models import Item,Order,OrderItem,Address,Payment,Coupon,Refund, UserProfile
from django.utils import timezone
from django.shortcuts import redirect
from django.urls import reverse
from .forms import CheckoutForm,CouponForm,RefundForm,PaymentForm
import stripe
import random 
import string
# Create your views here.

#stripe.api_key = settings.STRIPE_SECRET_KEY
#used for authenticate with stripe
stripe.api_key = 'sk_test_51HCND6DvfKocuQ5TJjkQabT2yyc4PoY7lzFdSENHqHYHn12Bc00vwy8JAUdORBBLqCPuLclKixBBKLVerIQBWkkg00ZsfFvjIx'
#stripe.api_key = 'pk_test_51HCND6DvfKocuQ5TITYZBNS0ie81ZauTA3kbq2tJ9PVynNyhgD0heP91NFfqlFcZqabmRIxK0pmcevrtJ0yBsPfK00gtOf4BPC'


def create_ref_code():
    #it would create a random seq of characters 
    #k =  special argument for length of string
    return ''.join(random.choices(string.ascii_lowercase + string.digits,k = 20))


class HomeView(ListView):
    model = Item
    paginate_by =10
    template_name = "home-page.html"


class OrderSummaryView(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        try:
            order = Order.objects.get(user=self.request.user,ordered=False)
            context = {
                'object': order
            }
            return render(self.request,'order_summary.html',context)
        except ObjectDoesNotExist:
            messages.warning(self.request,"You don't have any active order, Buy something first")
            return redirect("/")
    

class ItemDetailView(DetailView):
    model = Item
    template_name = "product-page.html"

#for validating the new shipping address taken in else statement of CheckoutView
#validating means that thee fields arent submitted empty
def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid


class CheckoutView(View):
    #get the request with arbitary no of arguments
    def get(self,*args,**kwargs):
        try:
        
            order = Order.objects.get(user=self.request.user,ordered=False)  
            #form
            form = CheckoutForm()
            context = {
                'form': form,
                'couponform':CouponForm(),
                'order':order,
                'DISPLAY_COUPON_FORM':True
                
            }

            shipping_address_qs = Address.objects.filter(
                user=self.request.user,
                address_type='S',
                default=True #we make default true when the user ticks the current address to be default
            )
            if shipping_address_qs.exists():
                context.update(
                    {
                        'default_shipping_address':shipping_address_qs[0] #q[0]=the first value inside the query set
                    }
                )

            billing_address_qs = Address.objects.filter(
                user=self.request.user,
                address_type='B',
                default=True #we make default true when the user ticks the current address to be default
            )
            if billing_address_qs.exists():
                context.update(
                    {
                        'default_billing_address':billing_address_qs[0] #[0]?
                    }
                )


            return render(self.request,"checkout.html",context)
        
        except ObjectDoesNotExist:
            messages.info(self.request,"You do not have any active order" )
            return redirect("/")
        

    def post(self,*args,**kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user,ordered=False)
            if form.is_valid():

                #check if we are using the default address
                #get the data from form ,if it is true the use default otherwise give in the info to form

                use_default_shipping = form.cleaned_data.get('use_default_shipping')
                #if the default address is used
                if use_default_shipping:
                    print("Using the default shipping address")
                    address_qs = Address.objects.filter(
                    user=self.request.user,
                    address_type='S',
                    default=True 
                    )
                    #checking if the user has a default address
                    if address_qs.exists():
                        shipping_address = address_qs[0] #here the shipping address would get filled withe default address used
                        order.shipping_address = shipping_address
                        order.save()
                       
                    else:
                        messages.info(self.request,"No default shipping address available")
                        return redirect("core:checkout")
                else:
                    print("user is entering a new shipping address")
                    

                    shipping_address1 = form.cleaned_data.get('shipping_address')
                    shipping_address2 = form.cleaned_data.get('shipping_address2')
                    shipping_country = form.cleaned_data.get('shipping_country')
                    shipping_zip = form.cleaned_data.get('shipping_zip')

                    if is_valid_form([shipping_address1,shipping_country,shipping_zip]):
                        shipping_address = Address(
                            user = self.request.user,
                            street_address=shipping_address1,
                            house_address = shipping_address2,
                            country = shipping_country,
                            zip = shipping_zip,
                            address_type='S'
                        )
                        shipping_address.save()


                         #order.shipping_address= field of order model saving the address in database
                        #shipping_address is the field of form in which the data is put and below we store that data in db
                        order.shipping_address = shipping_address
                        order.save()

                        #check if the current is set an nwe default
                        set_default_shipping = form.cleaned_data.get('set_default_shipping')
                        if set_default_shipping:
                            #shipping address is field of order model which has a relation with default field address model 
                            shipping_address.default= True
                            shipping_address.save()
                    else:
                        message.info(self.request,"Please fill in the required shipping address fields")
             
                
                use_default_billing = form.cleaned_data.get('use_default_billing')
                same_billing_address =form.cleaned_data.get('same_billing_address')#obj not callable error if get is nt written

               #checking first if the user has same billing address as shipping address
                if same_billing_address:
                    billing_address = shipping_address
                    billing_address.pk = None #for cloning it and not simply taking the orgnal value
                    billing_address.save() #we save so that a new address is created in db which = to the current  shipping address
                    billing_address.address_type = 'B' #changing the type to billing
                    billing_address.save() #saving it now as a billing address
                    order.billing_address = billing_address #we associate the blng addrs to the current order
                    order.save() # then here save it onto the order


               
                #if the default address is used
                elif use_default_billing:
                    print("Using the default billing address")
                    address_qs = Address.objects.filter(
                        user=self.request.user,
                        address_type='B',
                        default=True 
                    )
                    #checking if the user has a default address
                    if address_qs.exists():
                        billing_address = address_qs[0] #here the shipping address would get filled withe default address used
                        order.billing_address = billing_address
                        order.save()
                    else:
                        messages.info(self.request,"No default billing address available")
                        return redirect("core:checkout")
                else:
                    print("user is entering a new billing address")
                    

                    billing_address1 = form.cleaned_data.get('billing_address')
                    billing_address2 = form.cleaned_data.get('billing_address2')
                    billing_country = form.cleaned_data.get('billing_country')
                    billing_zip = form.cleaned_data.get('billing_zip')

                    if is_valid_form([billing_address1,billing_country,billing_zip]):
                        billing_address = Address(
                            user = self.request.user,
                            street_address=billing_address1,
                            house_address = billing_address2,
                            country = billing_country,
                            zip = billing_zip,
                            address_type='B'
                        )
                        billing_address.save()


                         #order.shipping_address= field of order model saving the address in database
                        #shipping_address is the field of form in which the data is put and below we store that data in db
                        order.billing_address = billing_address
                        order.save()

                        #check if the current is set an nwe default
                        set_default_billing = form.cleaned_data.get('set_default_billing')
                        if set_default_billing:
                            #billing address is field of order model which has a relation with default field address model 
                            billing_address.default= True
                            billing_address.save()
                    else:
                        messages.info(self.request,"Please fill in the required billing address fields")

                payment_option = form.cleaned_data.get('payment_option')

                if payment_option == 'S':
                    return redirect('core:payment',payment_option='stripe')
                elif payment_option == 'P':
                    return redirect('core:payment',payment_option='paypal')
                elif payment_option == 'C':
                    #creating payment
                    payment = Payment() 
                    payment.stripe_charge_id = random.vonmisesvariate(0,4)
                    payment.user = self.request.user
                    payment.amount  = order.get_total()
                    payment.save() 
                    
                    ######for fixing the order quantity for next order of same item#####
                    order_items = order.items.all()
                    order_items.update(ordered=True)
                    #doing the loop for each orderitem 
                    for item in order_items:
                        item.save()
                    ##########fixing end ############################
                    #assigning the payment to order
                    order.ordered =True
                        #this is the payment field of order model 
                    order.payment = payment
                    order.ref_code =create_ref_code()
                    order.being_delivered=True
                    order.save()
                    messages.success(self.request,"Your order has been successfully placed, keep your Cash ready at the time of delivery")
                    return redirect("/",payment_option='Cash-On-Delivery')
                    

                elif payment_option == 'D':
                    return redirect('core:payment',payment_option='Debitcard')
                else:
                    messages.warning(self.request,"invalid payment option")
                    return redirect("core:checkout")

        except ObjectDoesNotExist:
            messages.warning(self.request,"You don't have any active order, add something to your cart first")
            return redirect("core:order-summary")
        print(self.request.POST)


class PaymentView(View):
    def get(self, *args,**kwargs):
        order = Order.objects.get(user=self.request.user,ordered=False)
        #restricting to go to payment pg without a billing address
        if order.billing_address:
            context = {
                'order': order,
                'DISPLAY_COUPON_FORM':False,
                'STRIPE_PUBLIC_KEY' : 'pk_test_51HCND6DvfKocuQ5TITYZBNS0ie81ZauTA3kbq2tJ9PVynNyhgD0heP91NFfqlFcZqabmRIxK0pmcevrtJ0yBsPfK00gtOf4BPC'
            }
            #userprofile at right is a object of UserProfile class
            try:
                userprofile = self.request.user.userprofile
            except Exception as e:
                # Something else happened, 
                messages.warning(self.request,"You are logged in as an admin user, please login as a casual user")
                return redirect("/")

            if userprofile.one_click_purchasing:
                #fetch the users card list
                cards = stripe.Customer.list_sources(
                    userprofile.stripe_customer_id,
                    limit =3, #no of cards you want back from stripe api of that particular customer
                    object='card' #object is specified as filtering for card only as stripe can have other info too

                )
                card_list = cards['data']
                if len(card_list)>0:
                    #update the the context with default card
                    context.update({
                        'card' : card_list[0] # the first list item of cards_list
                    })

            return render(self.request,"payment.html",context)
        else:
            messages.warning(self.request,"You have not added a billing address")
            return redirect("core:checkout")
            

    def post(self, *args,**kwargs):
        #we get the order so that we can get the total amount for the order done below in our amount variable
        order = Order.objects.get(user=self.request.user,ordered=False)
        form = PaymentForm(self.request.POST)
        userprofile= UserProfile.objects.get(user=self.request.user)
        if form.is_valid():
            #stripetoken is a token ID  that we insert into the form so it gets submitted to the server
            token = form.cleaned_data.get('stripeToken')
            save = form.cleaned_data.get('save') #if user wants to save the current card
            use_default = form.cleaned_data.get('use_default')
        
            if save:
               #allow to fetch previous cards
               #this if check userprofile is not created then creates one
                if userprofile.stripe_customer_id != '' and userprofile.stripe_customer_id is not None:
                    customer = stripe.Customer.retrieve(
                        userprofile.stripe_customer_id)
                    customer.sources.create(source=token)

                   #here we get the id and save it in db via userprofile model
                    userprofile.stripe_customer_id = customer ['id']
                    userprofile.one_click_purchasing =True
                    userprofile.save()
                else: #if the userprofile is created we just need the id of that user and this would basclly add a new source i.e token to the user
                    customer = stripe.Customer.create(
                        email=self.request.user.email,
                    )
                    customer.sources.create(source=token)
                    userprofile.stripe_customer_id = customer['id']
                    userprofile.one_click_purchasing = True
                    userprofile.save()


            amount = int(order.get_total() * 100)  #we multiply by 100 bcoz the orgnal value is in paisa so to convert it to rupees

  #################################STRIPE ERROR PART CHANGES START####################################################     
       #create the payment,here we create payment as the object of the class (Model)Payment in Models.py
        payment = Payment() 
        payment.stripe_charge_id = random.vonmisesvariate(0,4)
        payment.user = self.request.user
        payment.amount  = order.get_total()
        payment.save() 
        
       
        # assign the payment to the order
        #when we recieve the post req we not only create a charge(as done above)
        #but we need to create a logic for which it says the order has been successfully ordered

        order_items = order.items.all()
        order_items.update(ordered=True)

        #doing the loop for each orderitem 
        for item in order_items:
            item.save()

        order.ordered =True
            #this is the payment field of order model 
        order.payment = payment
        order.ref_code =create_ref_code()
        order.being_delivered=True
        order.save()
  ##################################### ERROR CHANGES END ###############################################3

        try:
            # Use Stripe's library to make requests..
            if use_default or save: #this would be true if user has a profile
                charge = stripe.Charge.create(
                    amount=amount,
                    currency="usd",
                    customer=userprofile.stripe_customer_id
                
                )  
            else: #this would be running when anonymous purchase is done
                charge = stripe.Charge.create(
                    amount=amount,
                    currency="usd",
                    source=token                
                )  

            #######    HERE WOULD BE ERROR ABOVE THINGS PLACED IF API ERROR IS CORRECTED ##########
       
                    


           #######################   PLACE END  ###########################
                            
            messages.success(self.request,"Your order has been successfully placed, be ready for delivery soon")
        #redirect is used to go back to homepage after order succesffuly placed
            return redirect("/")

        except stripe.error.CardError as e:
        # Since it's a decline, stripe.error.CardError will be caught
        #we caught the error using json_body
            body = e.json_body
            err = body.get('error',{})
            messages.warning(self.request,f"{err.get('message')}")
        #redirect is used to go back to homepage after order succesffuly placed
            return redirect("/")
                            
        except stripe.error.RateLimitError as e:
        # Too many requests made to the API too quickly
            messages.warning(self.request,"Rate limit error")
            return redirect("/")
                        
        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            messages.success(self.request,"Your order has been successfully placed, be ready for delivery soon")
            return redirect("/")

        except stripe.error.AuthenticationError as e:
        # Authentication with Stripe's API failed
        # (maybe you changed API keys recently)
            messages.warning(self.request,"Not authenticated")
            return redirect("/")
                        
        except stripe.error.APIConnectionError as e:
        # Network communication with Stripe failed
            messages.warning(self.request,"Network error")
            return redirect("/")
                        
        except stripe.error.StripeError as e:
        # Display a very generic error to the user, and maybe send
        # yourself an email
            messages.warning(self.request,"Something went wrong. You were not charged, please try again")
            return redirect("/")

        except Exception as e:
                        # Something else happened, completely unrelated to Stripe
            messages.warning(self.request,"A serious error occured, we have notified the developers")
            return redirect("/")
                    


      

       


   

#slug is used here to identify a specific item
@login_required
def add_to_cart(request,slug):
    item = get_object_or_404(Item,slug=slug)
    #arg to get the specified item,then to get the user who has ordered,then last arg makes sure that we arnt getting a item 
    #that is already been purchase
    #as this returning a tuple we use two variables here
    order_item, created= OrderItem.objects.get_or_create(
        item=item,
        user = request.user,
        ordered=False
    )
    #we are filtering it so that we get the orders which are not completed as there can b orders which are compltd
    #and ordered field specifies orders whuch are compltd
    order_qs = Order.objects.filter(user=request.user,ordered=False)
    #if order exists
    if order_qs.exists():
        order = order_qs[0]
        #check if the order item is in the order
        if order.items.filter(item__slug =item.slug).exists():
            #if the above condtn is met that means the item is already in the cart
            order_item.quantity += 1
            order_item.save()
            messages.info(request,"Item quantity was updated" )
            return redirect("core:order-summary")
        #if there isnt a order yet
        #it redirects to the same pg if it is the first order of the item
        else:
            messages.info(request,"Item added to cart" )
            order.items.add(order_item)
            return redirect("core:product",slug=slug)

            

    #if order doesnt exists      
    else:
        ordered_date =timezone.now()
        order = Order.objects.create(user=request.user,ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request,"This item was added to your cart Boss." )
        #as this is a redirect func so kwargs not used but directly slug =slug
        return redirect("core:order-summary")

@login_required
def remove_from_cart(request,slug):
    item = get_object_or_404(Item,slug=slug)
    
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
        )

    #if order exists
    if order_qs.exists():
        #get that order
        order = order_qs[0]
        #check if the order item is in the order
        if order.items.filter(item__slug =item.slug).exists():
            order_item = OrderItem.objects.get_or_create(
                item=item,
                user = request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            messages.info(request,"This item was removed from your cart Boss." )
            return redirect("core:order-summary")
        else:
            #add a msg saying the order does not contain the item
            messages.info(request,"This item was not in your cart Boss." )
            return redirect("core:product",slug=slug)
    else:
        #add amsg saying the user doesnt hve an order
        messages.info(request,"You do not have an active order" )
        return redirect("core:product",slug=slug)

    
@login_required
def remove_single_item_from_cart(request,slug):
    item = get_object_or_404(Item,slug=slug)
    
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
        )

    #if order exists
    if order_qs.exists():
        #get that order
        order = order_qs[0]
        #check if the order item is in the order
        if order.items.filter(item__slug =item.slug).exists():
            order_item = OrderItem.objects.get_or_create(
                item=item,
                user = request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request,"The item quantity was updated" )
            #we dont pass a slug here as order-summry url doesnt use slug 
            return redirect("core:order-summary")
        else:
            #add a msg saying the order does not contain the item
            messages.info(request,"This item was not in your cart" )
            return redirect("core:product",slug=slug)
    else:
        #add amsg saying the user doesnt hve an order
        messages.info(request,"You do not have any active order" )
        return redirect("core:product",slug=slug)


#func for getting coupon in Addcoupon view

def get_coupon(request,code):
	coupon = Coupon.objects.get(code=code)
	return coupon

#imp :we cant send a get request to the below class based view because we havnt defined a get func in it
class AddCouponView(View):
    ####for validation of form###
    ##here self is used to get the current instance of the class and access varbles of this class rather than the inherited View
    def post(self, *args, **kwargs):
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
        #############validation ends####
            try:
                code =form.cleaned_data.get('code')
                order = Order.objects.get(user=self.request.user,ordered=False)
                order.coupon =get_coupon(self.request,code)
                order.save()
                messages.success(self.request,"Coupon applied successfully" )
                return redirect("core:checkout")

            except ValueError:
                messages.info(self.request,"The Promo-Code entered is Invalid" )
                return redirect("core:checkout")
				
            except ObjectDoesNotExist:
                messages.info(self.request,"The Promo-Code entered is Invalid" )
                return redirect("core:checkout")
        
   
class RequestRefundView(View):
    def get(self, *args, **kwargs):
        form = RefundForm()
        context = {
            'form' : form
        }
        return render(self.request,'request_refund.html',context)
    def post(self, *args, **kwargs):
        form =RefundForm(self.request.POST)
        if form.is_valid():
            #data from user in form 
            ref_code = form.cleaned_data.get('ref_code')
            message= form.cleaned_data.get('message')
            email =form.cleaned_data.get('email')
             #edit the order
            try:
                order = Order.objects.get(ref_code=ref_code)
                order.refund_requested=True
                order.save()

                #store the refund
                refund= Refund()
                refund.order = order
                refund.reason = message
                refund.email = email
                refund.save()

                messages.info(self.request,"Your request is really important to us, We will work on it ASAP!")
                return redirect("core:request-refund")

            
            except ObjectDoesNotExist:
                messages.info(self.request,"This Order Does Not Exist")
                return redirect("core:request-refund")


from allauth.account.forms import SignupForm
#study
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
class MyCustomSignupForm(CreateView):
    def random_sign(request):
        try:
            form_class =SignupForm
           # success_url = reverse_lazy('/')
            template_name = 'signup.html'
            return redirect("/")
        except Exception as e:
            # Something else happened, 
            messages.warning(self.request,"You are logged in as admin user, Please login as casual user")
            return redirect("/")
            

   
   
   
   # def save(self, request):

        # Ensure you call the parent class's save.
        # .save() returns a User object.
    #    user = super(MyCustomSignupForm, self).save(request)

        # Add your own processing here.

        # You must return the original result.
     #   return user